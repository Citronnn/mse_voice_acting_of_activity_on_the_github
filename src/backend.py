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
from json import dumps,loads
from json.decoder import JSONDecodeError
from websocket_server import WebsocketServer, WebSocketHandler
from pprint import pprint


event_queue: List[Event] = []
list_to_send: List[dict] = []
lock: Lock = Lock()


def get_current_time(git_time) -> datetime:
    now: datetime = datetime.now() - timedelta(hours=3, minutes=5)
    time_to_send = datetime(now.year, now.month, now.day,
                            git_time.hour, git_time.minute, git_time.second)
    return time_to_send + timedelta(hours=3, minutes=5, seconds=30)


def split_repo_name(full_repo_name):
    repo_owner, repo_subname = full_repo_name.split('/', 1)
    return repo_owner, repo_subname


def download_events():
    global event_queue

    print('Download events started')

    git = GitHub(token="78424da6d275052ec0cd159497b68ff34c06b1f2")
    print("Requests remaining this hour:", git.ratelimit_remaining, '\n')

    last_event = None
    while True:
        try:
            new_events: List[Event] = []
            for event in git.all_events():
                if last_event is None or event.id != last_event.id:
                    new_events += [event]
                else:
                    break
            last_event = new_events[0]
            event_queue[0:0] = new_events
        except ServerError:
            print("Server error occurred")
        except ConnectionError:
            print("Connection error occurred")
        except ConnectionAbortedError:
            print("Connection aborted error occurred")

        pushes = sum(event.type == "PushEvent" for event in event_queue)
        print(f'{event_queue[-1].created_at.time()}-'
              f'{event_queue[0].created_at.time()}, '
              f'events: {len(event_queue)}, '
              f'pushes: {pushes}')

        sleep(10)


def handle_events():
    global event_queue, list_to_send, lock

    print('Handle events started')

    while True:
        if len(event_queue) == 0:
            sleep(1)
            continue

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

                with lock:
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

                with lock:
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

                time_created = event.created_at.time()
                event = event.as_dict()

                url = f'https://github.com/{event["repo"]["name"]}'

                full_name_repo = event['repo']['name']
                owner, repo = split_repo_name(full_name_repo)

                with lock:
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

                with lock:
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

                with lock:
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

                with lock:
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

                with lock:
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

                with lock:
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

                with lock:
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

                with lock:
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

        with lock:
            list_to_send_now = [i for i in list_to_send if i['time'] < now]
            list_to_send = [i for i in list_to_send if i['time'] >= now]

        for send_item in list_to_send_now:
            # print('send', send_item['time'])
            del send_item['time']
            server.broadcast(send_item)

        sleep(0.01)


class Debug:
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

    def finish(self):
        try:
            self.handler.finish()
        except KeyError:
            Debug.error(f'Key error possibly double '
                        f'deleting id = {self.id}')

    def send_raw(self, message: str) -> None:
        try:
            Debug.send(f'Send to {self.id}: {"{ JSON event }"}')
            self.handler.send_message(message)
        except BrokenPipeError:
            Debug.error(f'Broken pipe error send raw id = {self.id}')

    def send(self, obj: dict) -> None:
        try:
            msg = dumps(obj)
            #print(msg)
            Debug.send(f'Send to {self.id}: {"{ JSON event }"}')
            self.handler.send_message(msg)
        except BrokenPipeError:
            Debug.error(f'Broken pipe error send id = {self.id}')

    def receive(self, srv: 'Server', message: str, client: dict):
        print(message);
        if message[2:6] == 'type':
            msg = loads(message);
            if msg['type'] == 'filter' and len(msg['org']) and len(msg['repo']):
                if msg['org'][0]!='[' or msg['org'][-1]!=']':
                    if msg['repo'][0]!='[' or msg['repo'][-1]!=']':
                        self.send({'type': "error", 'where': ["org","repo"]});
                    else:
                        self.send({'type': "error", 'where': "org"});
                elif msg['repo'][0]!='[' or msg['repo'][-1]!=']':
                    self.send({'type': "error", 'where': "repo"});
                else:
                    print("Ok");
                    #Действия


    def left(self, srv: 'Server') -> None:
        del srv.clients[self.id]
        # Debug.client_left('DEL VISUAL GITHUB', self.id)


class Server:

    if Debug.Debug:
        ip = '127.0.0.1'
        local_ip = '127.0.0.1'

    else:
        ip = '188.134.82.95'
        local_ip = '192.168.0.100'

    port = 11001

    def __init__(self):

        self.server = WebsocketServer(Server.port, Server.local_ip)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)

        self.clients: Dict[int, VisualGithubClient] = {}

    def run(self):
        self.server.run_forever()

    # Called for every client connecting (after handshake)
    def new_client(self, client, _):
        Debug.connected(f'New client connected '
                        f'and was given id {client["id"]}')
        new_client = VisualGithubClient(client['id'], client['handler'])
        client['client'] = new_client
        self.clients[new_client.id] = new_client

    # Called for every client disconnecting
    def client_left(self, client, _):

        if client is None:
            return

        Debug.client_left(f'Client {client["id"]} disconnected')
        try:
            client['client'].left(self)
        except KeyError:
            Debug.error(f'Key error possibly double deleting '
                        f'in client left id = {client["id"]}')
        except ValueError:
            Debug.error(f'Value error possibly double deleting '
                        f'in client left id = {client["id"]}')

    # Called when a client sends a message
    def message_received(self, client, _, message):
        if client is None:
            return
        message = message.encode('ISO-8859-1').decode()
        client['client'].receive(self, message, client)

    def broadcast(self, message: dict):
        for client in list(self.clients.values()):
            client.send(message)

if __name__ == '__main__':
    server = Server()
    Thread(target=lambda: server.run(), name='WebSocket server').start()
    Thread(target=download_events, name="Download events").start()
    Thread(target=handle_events, name="Handle events").start()
    Thread(target=send_events, name="Send events").start()

    @route('/')
    def index():
        return template('frontend.html', ip=Server.ip, port=Server.port)

    @route('/<file:path>')
    def static_serve(file):
        return static_file(file, root='.')

    run(host=Server.local_ip, port=80)
