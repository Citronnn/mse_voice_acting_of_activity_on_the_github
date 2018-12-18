import re
from os import listdir
from os.path import isdir, isfile, join
from bottle import route, run, static_file, template
from github3 import GitHub
from github3.events import Event
from github3.exceptions import NotFoundError
from github3.exceptions import ServerError
from github3.exceptions import ConnectionError
from threading import Thread, Lock
from typing import List, Dict
from time import sleep
from datetime import datetime, timedelta
from json import dumps, loads
from json.decoder import JSONDecodeError
from websocket_server import WebsocketServer, WebSocketHandler
from pprint import pprint


event_queue: List[Event] = []
list_to_send: List[dict] = []
events_to_send_lock: Lock = Lock()
event_queue_lock: Lock = Lock()


def get_current_time(git_time) -> datetime:
    now: datetime = datetime.now() - timedelta(hours=3, minutes=5)
    time_to_send = datetime(now.year, now.month, now.day,
                            git_time.hour, git_time.minute, git_time.second)
    return time_to_send + timedelta(hours=3, minutes=5, seconds=30)


def split_repo_name(full_repo_name):
    repo_owner, repo_subname = full_repo_name.split('/', 1)
    return repo_owner, repo_subname


def remove_duplicates():
    if len(list_to_send) < 2:
        return

    duplicate = list_to_send[-1]
    for num, event in enumerate(list_to_send[-2::-1], 1):
        if event['type'] != duplicate['type']:
            continue
        if event['owner'] != duplicate['owner']:
            continue
        if event['repo'] != duplicate['repo']:
            continue
        if event['time'] != duplicate['time']:
            continue

        list_to_send.pop()
        return


def download_events():
    global event_queue

    print('Download events started')

    git = GitHub(token="78424da6d275052ec0cd159497b68ff34c06b1f2")
    print("Requests remaining this hour:", git.ratelimit_remaining, '\n')

    last_event = None
    seconds_to_sleep = 10
    while True:
        try:
            new_events: List[Event] = []
            need_skip = False
            need_reduce_sleep = False
            need_increase_sleep = False
            skipped_events = 0

            for event in git.all_events():
                if not need_skip:
                    if last_event is None or event.id != last_event.id:
                        new_events += [event]
                    else:
                        need_skip = True
                else:
                    skipped_events += 1

            if skipped_events == 0:
                need_reduce_sleep = True
            elif skipped_events > len(new_events):
                need_increase_sleep = True

            if need_reduce_sleep and seconds_to_sleep > 1:
                seconds_to_sleep -= 1
            if need_increase_sleep:
                seconds_to_sleep += 1

            if len(new_events):
                last_event = new_events[0]
            with event_queue_lock:
                event_queue[0:0] = new_events

        except ServerError:
            print("Server error occurred")
        except ConnectionError:
            print("Connection error occurred")
        except ConnectionAbortedError:
            print("Connection aborted error occurred")

        with event_queue_lock:
            if len(event_queue):
                pushes = sum(event.type == "PushEvent" for event in event_queue)
                print(f'{event_queue[-1].created_at.time()}-'
                      f'{event_queue[0].created_at.time()}, '
                      f'events: {len(event_queue):>3} '
                      f'pushes: {pushes:>3} '
                      f'sleep: {seconds_to_sleep:>2}s '
                      f'limit: {git.ratelimit_remaining:>4}')

        sleep(seconds_to_sleep)


def handle_events():
    global event_queue, list_to_send, events_to_send_lock

    print('Handle events started')

    while True:
        if len(event_queue) == 0:
            sleep(1)
            continue

        with events_to_send_lock:
            remove_duplicates()

        with event_queue_lock:
            event: Event = event_queue.pop()

        try:

            if event.type == 'PushEvent':

                if not (event.payload['size'] > 0 and event.public):
                    continue

                time_created = event.created_at.time()
                repo_name = event.repo['name']
                repo_owner, repo_subname = repo_name.split('/', 1)
                total_commits = len(event.payload['commits'])
                commit_hash = event.payload['commits'][-1]['sha']
                url = f'https://github.com/{repo_name}/commit/{commit_hash}'

                with events_to_send_lock:
                    list_to_send += [
                        {
                            'type': 'push',
                            'time': get_current_time(time_created),
                            'owner': repo_owner,
                            'repo': repo_subname,
                            'commits': total_commits,
                            'url': url,
                            'hash': commit_hash
                        }
                    ]

            elif event.type == 'PullRequestEvent':

                time_created = event.created_at.time()
                event = event.as_dict()

                url = event['payload']['pull_request']['html_url']
                author = event['actor']['login']
                title = event['payload']['pull_request']['title']
                commits = event['payload']['pull_request']['commits']
                changed = event['payload']['pull_request']['changed_files']

                full_name_repo = event['repo']['name']
                owner, repo = split_repo_name(full_name_repo)

                with events_to_send_lock:
                    list_to_send += [
                        {
                            'type': 'pull_request',
                            'time': get_current_time(time_created),
                            'owner': owner,
                            'repo': repo,
                            'commits': commits,
                            'url': url,
                            'author': author,
                            'title': title,
                            'changed_files': changed
                        }
                    ]

            elif event.type == 'CreateEvent':
                continue

                time_created = event.created_at.time()
                event = event.as_dict()

                url = f'https://github.com/{event["repo"]["name"]}'

                full_name_repo = event['repo']['name']
                owner, repo = split_repo_name(full_name_repo)

                with events_to_send_lock:
                    list_to_send += [
                        {
                            'type': 'create_repo',
                            'time': get_current_time(time_created),
                            'owner': owner,
                            'repo': repo,
                            'url': url
                        }
                    ]

            elif event.type == 'ForkEvent':

                time_created = event.created_at.time()
                event = event.as_dict()

                url = event['payload']['forkee']['html_url']
                full_name_repo = event['payload']['forkee']['full_name']
                owner, repo = split_repo_name(full_name_repo)

                with events_to_send_lock:
                    list_to_send += [
                        {
                            'type': 'fork_repo',
                            'time': get_current_time(time_created),
                            'owner': owner,
                            'repo': repo,
                            'url': url
                        }
                    ]

            elif event.type == 'WatchEvent':
                pass

            elif event.type == 'IssuesEvent':

                time_created = event.created_at.time()
                event = event.as_dict()
                url = event['payload']['issue']['html_url']
                owner, repo = split_repo_name(event['repo']['name'])

                with events_to_send_lock:
                    list_to_send += [
                        {
                            'type': 'issue',
                            'time': get_current_time(time_created),
                            'owner': owner,
                            'repo': repo,
                            'url': url
                        }
                    ]

            elif event.type == 'DeleteEvent':
                pass

            elif event.type == 'IssueCommentEvent':

                time_created = event.created_at.time()
                event = event.as_dict()
                owner, repo = split_repo_name(event['repo']['name'])
                url = event['payload']['comment']['html_url']

                with events_to_send_lock:
                    list_to_send += [
                        {
                            'type': 'issue_comment',
                            'time': get_current_time(time_created),
                            'owner': owner,
                            'repo': repo,
                            'url': url
                        }
                    ]

            elif event.type == 'PullRequestReviewCommentEvent':

                time_created = event.created_at.time()
                event = event.as_dict()
                owner, repo = split_repo_name(event['repo']['name'])
                url = event['payload']['comment']['html_url']

                with events_to_send_lock:
                    list_to_send += [
                        {
                            'type': 'pull_request_review',
                            'time': get_current_time(time_created),
                            'owner': owner,
                            'repo': repo,
                            'url': url
                        }
                    ]

            elif event.type == 'GollumEvent':

                time_created = event.created_at.time()
                event = event.as_dict()
                owner, repo = split_repo_name(event['repo']['name'])

                if len(event['payload']['pages']) == 0:
                    continue

                url = event['payload']['pages'][-1]['html_url']

                with events_to_send_lock:
                    list_to_send += [
                        {
                            'type': 'wiki_page',
                            'time': get_current_time(time_created),
                            'owner': owner,
                            'repo': repo,
                            'url': url
                        }
                    ]

            elif event.type == 'ReleaseEvent':

                time_created = event.created_at.time()
                event = event.as_dict()
                owner, repo = split_repo_name(event['repo']['name'])
                url = event['payload']['release']['html_url']

                with events_to_send_lock:
                    list_to_send += [
                        {
                            'type': 'release',
                            'time': get_current_time(time_created),
                            'owner': owner,
                            'repo': repo,
                            'url': url
                        }
                    ]

            elif event.type == 'PublicEvent':
                pass

            elif event.type == 'CommitCommentEvent':

                time_created = event.created_at.time()
                event = event.as_dict()
                owner, repo = split_repo_name(event['repo']['name'])
                url = event['payload']['comment']['html_url']

                with events_to_send_lock:
                    list_to_send += [
                        {
                            'type': 'commit_comment',
                            'time': get_current_time(time_created),
                            'owner': owner,
                            'repo': repo,
                            'url': url
                        }
                    ]

            elif event.type == 'MemberEvent':
                pass

            else:
                pprint(event.as_dict())
                pass

        except NotFoundError:
            pass

        except JSONDecodeError:
            pass


def send_events():

    print('Send events started')

    global list_to_send

    while True:

        for item in list_to_send:
            cur_time: datetime = item['time']
            same_time_list = [i for i in list_to_send if i['time'] == cur_time]
            if len(same_time_list) > 1:

                divider = len(same_time_list)
                for i, same_item in enumerate(same_time_list):
                    increase = timedelta(milliseconds=i / divider * 1000)
                    same_item['time'] += increase

        now = datetime.now()

        with events_to_send_lock:
            list_to_send_now = [i for i in list_to_send if i['time'] < now]
            list_to_send = [i for i in list_to_send if i['time'] >= now]

        for send_item in list_to_send_now:
            # print('send', send_item['time'])
            del send_item['time']
            websocket_server.broadcast(send_item)

        sleep(0.01)


class DebugLog:
    Debug = 1
    Send = 0
    Connected = 1
    ClientLeft = 1
    Errors = 1

    if Send:
        @staticmethod
        def send(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def send(*args, **kwargs):
            pass

    if Connected:
        @staticmethod
        def connected(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def connected(*args, **kwargs):
            pass

    if ClientLeft:
        @staticmethod
        def client_left(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def client_left(*args, **kwargs):
            pass

    if Errors:
        @staticmethod
        def error(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def error(*args, **kwargs):
            pass


class VisualGithubClient:

    def __init__(self, _id: int, handler: WebSocketHandler):
        # Это внутренний ID клиента, присваиваемый сервером
        self.id: int = _id
        self.handler: WebSocketHandler = handler
        self.owner_filter = re.compile('')
        self.repo_filter = re.compile('')
        self.type_filters = {
            'pull_request': False,
            'push': False,
            'issue': False,
            'fork_repo': False,
            'wiki_page': False,
            'release': False,
            'pull_request_review': False,
            'commit_comment': False,
            'issue_comment': False
        }

        self.send({
            'type': 'init',
            'categories': audio_lengths
        })

    def finish(self):
        try:
            self.handler.finish()
        except KeyError:
            DebugLog.error(f'Key error possibly double '
                           f'deleting id = {self.id}')

    def send(self, obj: dict) -> None:
        try:
            msg = dumps(obj)
            DebugLog.send(f'Send to {self.id}: {"{ JSON event }"}')
            self.handler.send_message(msg)
        except BrokenPipeError:
            DebugLog.error(f'Broken pipe error send id = {self.id}')

    def pass_filters(self, event: dict):
        return self.pass_type_filters(event) and self.pass_regexp_filters(event)

    def pass_type_filters(self, event: dict):
        return self.type_filters[event['type']]

    def set_type_filters(self, event: dict):
        del event['type']
        for curr_type in event:
            self.type_filters[curr_type] = event[curr_type]

    def pass_regexp_filters(self, event: dict):
        owner_match = self.owner_filter.fullmatch(event['owner']) is not None
        repo_match = self.repo_filter.fullmatch(event['repo']) is not None
        return owner_match and repo_match

    def set_regexp_filters(self, owner: str, repo: str):
        try:
            owner = owner.lower()
            if owner == '':
                owner = '.*'
            self.owner_filter = re.compile(owner, re.IGNORECASE)
        except re.error:
            self.send({
                'type': 'error',
                'where': 'owner'
            })

        try:
            repo = repo.lower()
            if repo == '':
                repo = '.*'
            self.repo_filter = re.compile(repo, re.IGNORECASE)
        except re.error:
            self.send({
                'type': 'error',
                'where': 'repo'
            })

    def receive(self, srv: 'WebSocketServer', message: str, client: dict):
        try:
            json_msg = loads(message)
            if json_msg['type'] == 'filter_regexp':
                self.set_regexp_filters(json_msg['owner'], json_msg['repo'])
            elif json_msg['type'] == 'filter_types':
                self.set_type_filters(json_msg)
        except JSONDecodeError:
            print('JSONDecodeError', message)

    def left(self, srv: 'WebSocketServer') -> None:
        del srv.clients[self.id]
        # Debug.client_left('DEL VISUAL GITHUB', self.id)


class WebSocketServer:

    if DebugLog.Debug:
        ip = '127.0.0.1'
        local_ip = '127.0.0.1'

    else:
        ip = '188.134.82.95'
        local_ip = '192.168.0.100'

    port = 11001

    def __init__(self):

        self.server = WebsocketServer(WebSocketServer.port, WebSocketServer.local_ip)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)

        self.clients: Dict[int, VisualGithubClient] = {}

    def run(self):
        self.server.run_forever()

    # Called for every client connecting (after handshake)
    def new_client(self, client, _):
        DebugLog.connected(f'New client connected '
                        f'and was given id {client["id"]}')
        new_client = VisualGithubClient(client['id'], client['handler'])
        client['client'] = new_client
        self.clients[new_client.id] = new_client

    # Called for every client disconnecting
    def client_left(self, client, _):

        if client is None:
            return

        DebugLog.client_left(f'Client {client["id"]} disconnected')
        try:
            client['client'].left(self)
        except KeyError:
            DebugLog.error(f'Key error possibly double deleting '
                           f'in client left id = {client["id"]}')
        except ValueError:
            DebugLog.error(f'Value error possibly double deleting '
                           f'in client left id = {client["id"]}')

    # Called when a client sends a message
    def message_received(self, client, _, message):
        if client is None:
            return
        message = message.encode('ISO-8859-1').decode()
        client['client'].receive(self, message, client)

    def broadcast(self, message: dict):
        for client in list(self.clients.values()):
            if client.pass_filters(message):
                client.send(message)


def get_audio_files():
    files = {}
    for folder in listdir('audio'):
        full_folder = join('audio', folder)
        if not isdir(full_folder):
            continue
        for file in listdir(full_folder):
            full_file = join(full_folder, file)
            if not isfile(full_file) or not file.endswith('.mp3'):
                continue
            if folder not in files:
                files[folder] = []
            files[folder] += [full_file]
    return files


if __name__ == '__main__':

    websocket_server = WebSocketServer()
    Thread(target=lambda: websocket_server.run(), name='WebSocket server').start()
    Thread(target=download_events, name="Download events").start()
    Thread(target=handle_events, name="Handle events").start()
    Thread(target=send_events, name="Send events").start()

    audio_files = get_audio_files()
    audio_lengths = {folder: len(files) for folder, files in audio_files.items()}
    audio_lengths = dumps(audio_lengths)

    @route('/')
    def index():
        return template('frontend.html',
                        ip=WebSocketServer.ip,
                        port=WebSocketServer.port)

    @route('/<file:path>')
    def static_serve(file: str):
        if file.endswith('.mp3'):
            path = file.split('/')
            filename = path[-1]
            folder = path[-2]
            file_num = filename.split('.')[0]  # without ".mp3"
            file = audio_files[folder][int(file_num)]

        return static_file(file, root='.')

    run(host=WebSocketServer.local_ip, port=80)
