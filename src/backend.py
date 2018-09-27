from github3 import GitHub
from github3.events import Event
from github3.search import CommitSearchResult
from github3.exceptions import NotFoundError
from github3.exceptions import ServerError
from github3.exceptions import ConnectionError
from github3.git import ShortCommit
from github3.repos.repo import Repository
from github3.repos.commit import RepoCommit
from pprint import pprint
from threading import Thread
from typing import List
from time import sleep
from datetime import datetime
from json import load, dump, loads, dumps
from websocket_server import WebsocketServer, WebSocketHandler

git = GitHub(token="78424da6d275052ec0cd159497b68ff34c06b1f2")
print("Requests remaining this hour:", git.ratelimit_remaining, '\n')

event_queue: List[Event] = []
loop = 0


def download_events():
    global event_queue, loop

    print('Download events started')

    last_event = None
    while True:
        try:
            new_events: List[Event] = []
            for event in git.all_events():
                event: Event
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

        sleep(10)
        print(str(datetime.now())[:-7], loop)


def handle_events():
    global event_queue, loop

    print('Handle events started')

    logins_path = 'files/logins.json'
    repos_path = 'files/repos.json'
    repositories_path = 'files/repositories.json'

    logins = load(open(logins_path))
    repos = load(open(repos_path))
    repositories = {k: set(v['list']) for k, v in load(open(repositories_path)).items()}
    loop = 0
    while True:
        if len(event_queue) == 0:
            sleep(1)
            continue

        loop += 1
        if loop % 1000 == 0:
            print()
            sorted_logins = sorted([x for x in logins.items()], key=lambda x: -x[1])
            for place, (login, value) in enumerate(sorted_logins[:10], 1):
                repo_info = repos[login]
                repo_max = max([x for x in repo_info.items()], key=lambda x: x[1])
                print(place, login, value,
                      f'| {repo_max[0]}'
                      f'{"" if len(repo_info) == 1 else f": {repo_max[1]} ... {len(repo_info) - 1} more"}')
            print("\nRequests remaining this hour:", git.ratelimit_remaining, '\n')
            dump(logins, open(logins_path, 'w'), indent=4)
            dump(repos, open(repos_path, 'w'), indent=4)
            dump({k: {'total': len(v), 'list': list(v)} for k, v in repositories.items()},
                 open(repositories_path, 'w'), indent=4)

        event: Event = event_queue.pop()
        if event.type == 'PushEvent' and event.payload['size'] > 0 and event.public:
            try:
                time_created = event.created_at.time()
                repo_name = event.repo['name']
                repo_id = event.repo['id']
                repo_owner, repo_subname = repo_name.split('/', 1)
                # print(repo_main)
                # repository = git.repository_with_id(repo_id)
                # total_commits = event.payload['size']
                total_commits = len(event.payload['commits'])
                commit_hash = event.payload['commits'][-1]['sha']
                url = f'https://github.com/{repo_name}/commit/{commit_hash}'
                # print(time_created, event.type, total_commits, event.repo['name'], url)
                # if event.payload['size'] > 1:
                #     print(event.payload['size'], event.payload['distinct_size'], len(event.payload['commits']))

                # repository: Repository = git.repository_with_id(repo_id)
                # commit: RepoCommit = repository.commit(commit_hash)
                # print(commit.last_modified)
                # print(commit.additions)
                # print(commit.deletions)

                logins[repo_owner] = logins.get(repo_owner, 0) + total_commits

                repos_info = repos.get(repo_owner, {})
                if repo_subname not in repos_info.keys():
                    repos_info[repo_subname] = 0
                repos_info[repo_subname] = repos_info.get(repo_subname, 0) + total_commits
                repos[repo_owner] = repos_info

                for commit in event.payload['commits']:
                    repositories[repo_subname] = repositories.get(repo_subname, set()) | {commit['sha']}

            except NotFoundError:
                pass
        else:
            # print(event.type)
            pass


class Debug:
    Debug = 0
    Send = 1
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


class AbstractClient:

    class ID:
        VisualGithub = 'vg'

    def __init__(self, _id: int, name: str, handler: WebSocketHandler):
        self.id: int = _id  # Это внутренний ID клиента, присваиваемый сервером
        self.name = name
        self.handler: WebSocketHandler = handler

    def finish(self):
        try:
            self.handler.finish()
        except KeyError:
            Debug.error(f'Key error possibly double deleting id = {self.id}')

    def send_raw(self, message: str) -> None:
        try:
            Debug.send(f'Send to {self.id}: {message}')
            self.handler.send_message(message)
        except BrokenPipeError:
            Debug.error(f'Broken pipe error send raw id = {self.id}')

    def send(self, obj: dict) -> None:
        try:
            msg = dumps(obj)
            Debug.send(f'Send to {self.id}: {msg}')
            self.handler.send_message(msg)
        except BrokenPipeError:
            Debug.error(f'Broken pipe error send id = {self.id}')

    def receive(self, srv: 'Server', message: str, client: dict) -> None:
        raise NotImplementedError('Method "receive" is not implemented in derived class')

    def left(self, srv: 'Server') -> None:
        raise NotImplementedError('Method "left" is not implemented in derived class')


class VisualGithubClient(AbstractClient):

    def __init__(self, _id: int, handler: WebSocketHandler):
        super().__init__(_id, AbstractClient.ID.VisualGithub, handler)

    def receive(self, srv: 'Server', message: str, client: dict):
        pass

    def left(self, srv: 'Server') -> None:
        Debug.client_left('DEL VISUAL GITHUB', self.id)




Thread(target=download_events, name="Download events").start()
Thread(target=handle_events, name="Handle events").start()


print("\nRequests (after) remaining this hour:", git.ratelimit_remaining)


def check(reply: str, clue: str):
    lines = [i.strip() for i in reply.splitlines()]
    first_line_length = len(lines[0])
    if not all(len(line) == first_line_length for line in lines[1:]):
        return False
    if set("".join(lines)) != 2:
        return False
    return True
