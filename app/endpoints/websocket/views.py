# -*- coding: utf-8 -*-
from enum import Enum
from typing import List

from fastapi import APIRouter
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.endpoints import WebSocketEndpoint
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse
from starlette.types import ASGIApp
from starlette.types import ASGIInstance
from starlette.types import Scope
from starlette.websockets import WebSocket

router = APIRouter()
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_methods=["*"]
)


html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>FastAPI Websocket Chat</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <style>
        #main {
            margin-top: 4rem;
        }
        #chatbox {
            overflow-y: scroll;
            height: 40rem;
        }
        .thin-alert {
            padding: .25rem 1.25rem;
        }
    </style>
  </head>
  <body>
    <div class="container">
        <div id="main" class="row">
            <div class="col-md-9">
                <h4>Chat</h4>
                <div id="chatbox">
                    <div id="messages"></div>
                </div>
                <form>
                    <div class="form-group row">
                        <label for="chat-input" class="col-sm-1 col-form-label">Message</label>
                        <div class="col-sm-9">
                            <input type="text" class="form-control" id="chat-input" placeholder="Enter message...">
                        </div>
                        <div class="col-sm-2">
                            <button type="submit" class="btn btn-primary" disabled="disabled">Send</button>
                        </div>
                    </div>
                </form>
            </div>
            <div class="col-md-3">
                <h4>Connected Users</h4>
                <ul id="users"></ul>
            </div>
      </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script>
    /** Add a user to the list of connected users.*/
    function addToUsersList(userId, isYou) {
        const newUserLi = $('<li id="users-list-' + userId + '"></li>');
        newUserLi.append(userId);
        if(isYou) {
            newUserLi.append($('<em> (you)</em>'));
        }
        $('#users').append(newUserLi);
    }
    /** Add a user to the list of connected users and print an alert.*/
    function addUser(userId) {
        console.log('Adding user to connected users list:', userId);
        addToUsersList(userId);
        addSystemMessage($('<span>User <strong>' + userId + '</strong> joined the room</span>'));
    }
    /** Remove a user from the list of connected users and print an alert.*/
    function removeUser(userId) {
        console.log('Removing user from connected users list:', userId);
        $('li#users-list-' + userId).remove();
        addSystemMessage($('<span>User <strong>' + userId + '</strong> left the room</span>'));
    }
    /** Add a new chat message from a named user. */
    function addChatMessage(userId, msg) {
        const newMessage = $('<div class="alert thin-alert" role="alert"></div>');
        const userSays = $('<strong>' + userId + ':  </strong>');
        if(userId === myUserId) {
            newMessage.addClass('alert-secondary');
        } else {
            newMessage.addClass('alert-info');
        }
        newMessage.append(userSays);
        newMessage.append(msg);
        $('#messages').append(newMessage);
    }
    /** Add a new system message (e.g. user joined/left) to the chat. */
    function addSystemMessage(msg) {
        const newMessage = $('<div class="alert thin-alert alert-success" role="alert"></div>');
        newMessage.append(msg);
        $('#messages').append(newMessage);
    }

    /** Add a new error message to the chat. */
    function addErrorMessage(msg) {
        const newMessage = $('<div class="alert thin-alert alert-danger" role="alert"></div>');
        newMessage.append(msg);
        $('#messages').append(newMessage);
    }
    /** Handle an incoming message from the websocket connection. */
    function onWebsocketMessage(message) {
        console.log('Got message from websocket:', message);
        const payload = JSON.parse(message.data);
        switch(payload.type) {
            case 'MESSAGE':
                if(payload.data.user_id === 'server') {
                    addSystemMessage(payload.data.msg);
                } else {
                    addChatMessage(payload.data.user_id, payload.data.msg);
                }
                return;
            case 'USER_JOIN':
                addUser(payload.data);
                return;
            case 'USER_LEAVE':
                removeUser(payload.data);
                return;
            case 'ROOM_JOIN':
                myUserId = payload.data.user_id;
                addToUsersList(myUserId, true);
                return;
            default:
                throw new TypeError('Unknown message type: ' + payload.type);
                return;
        }
    }

    function onClickFactory(websocket) {
        return function (event) {
            event.preventDefault();
            const $messageInput = $('#chat-input');
            const message = $messageInput.val();
            $messageInput.val('');
            if (!message) {
                return
            }
            websocket.send(message);
        }
    }
    /** Join up the 'submit' button to the websocket interface. */
    function onWebsocketOpen(websocket) {
        return function () {
            $('button[type="submit"]')
                .on('click', onClickFactory(websocket))
                .removeAttr('disabled');
        }
    }
    /** Print websocket errors into the chat box using addErrorMessage. */
    function onWebsocketError(err) {
        console.error('Websocket error: ', err);
        addErrorMessage('Error:' + err, 'error');
        onWebsocketClose();
    }
    /** Disable the 'submit' button when the websocket connection closes. */
    function onWebsocketClose() {
        $('button[type="submit"]')
            .off('click')
            .attr('disabled', 'disabled');
    }
    /** On page load, open a websocket connection, and fetch the list of active users. */
    $(function() {
        function reqListener () {
            const userList = JSON.parse(this.responseText);
            console.log('Received user list:', userList);
            userList.forEach(addToUsersList);
            $(function() {
                let myUserId = null;
                websocket = new WebSocket('ws://localhost:5000/api/v1/websocket/ws');
                websocket.onopen = onWebsocketOpen(websocket);
                websocket.onerror = onWebsocketError;
                websocket.onclose = onWebsocketClose;
                websocket.onmessage = onWebsocketMessage;
            });
        }
        const oReq = new XMLHttpRequest();
        oReq.addEventListener("load", reqListener);
        oReq.open("GET", "http://localhost:5000/api/v1/websocket/list_users");
        oReq.send();
    });
    </script>
  </body>
</html>
"""


class Room:
    """Room state, comprising connected users.
    """

    def __init__(self):
        self._users = {}

    def __len__(self) -> int:
        """Get the number of users in the room.
        """
        return len(self._users)

    @property
    def empty(self) -> bool:
        """Check if the room is empty.
        """
        return len(self._users) == 0

    @property
    def user_list(self) -> List[str]:
        """Return a list of IDs for connected users.
        """
        return list(self._users)

    def add_user(self, user_id: str, websocket: WebSocket):
        """Add a user websocket, keyed by corresponding user ID.
        Raises:
            ValueError: If the `user_id` already exists within the room.
        """
        if user_id in self._users:
            raise ValueError(f"User {user_id} is already in the room")
        self._users[user_id] = websocket

    def remove_user(self, user_id):
        """Remove a user from the room.
        Raises:
            ValueError: If the `user_id` is not held within the room.
        """
        if user_id not in self._users:
            raise ValueError(f"User {user_id} is not in the room")
        del self._users[user_id]

    async def whisper(self, from_user: str, to_user: str, msg: str):
        """Send a private message from one user to another.
        Raises:
            ValueError: If either `from_user` or `to_user` are not present
                within the room.
        """
        if from_user not in self._users:
            raise ValueError(f"Calling user {from_user} is not in the room")
        if to_user not in self._users:
            await self._users[from_user].send_json(
                {
                    "type": "ERROR",
                    "data": {"msg": f"User {to_user} is not in the room!"},
                }
            )
            return
        await self._users[to_user].send_json(
            {
                "type": "WHISPER",
                "data": {"from_user": from_user, "to_user": to_user, "msg": msg},
            }
        )

    async def broadcast_message(self, user_id: str, msg: str):
        """Broadcast message to all connected users.
        """
        for websocket in self._users.values():
            await websocket.send_json(
                {"type": "MESSAGE", "data": {"user_id": user_id, "msg": msg}}
            )

    async def broadcast_user_joined(self, user_id: str):
        """Broadcast message to all connected users.
        """
        for websocket in self._users.values():
            await websocket.send_json({"type": "USER_JOIN", "data": user_id})

    async def broadcast_user_left(self, user_id: str):
        """Broadcast message to all connected users.
        """
        for websocket in self._users.values():
            await websocket.send_json({"type": "USER_LEAVE", "data": user_id})


class RoomEventMiddleware:
    """Middleware for providing a global :class:`~.Room` instance to both HTTP
    and WebSocket scopes.
    Although it might seem odd to load the broadcast interface like this (as
    opposed to, e.g. providing a global) this both mimics the pattern
    established by starlette's existing DatabaseMiddlware, and describes a
    pattern for installing an arbitrary broadcast backend (Redis PUB-SUB,
    Postgres LISTEN/NOTIFY, etc) and providing it at the level of an individual
    request.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self._room = Room()

    def __call__(self, scope: Scope) -> ASGIInstance:
        if scope["type"] in ("lifespan", "http", "websocket"):
            scope["room"] = self._room
        return self.app(scope)


app.add_middleware(RoomEventMiddleware)


@router.get("/")
def home():
    return FileResponse("static/index.html")


@router.get("/list_users")
async def list_users(request: Request):
    """Broadcast an ambient message to all chat room users.
    """
    return request.get("room").user_list


class Distance(str, Enum):
    Near = "near"
    Far = "far"
    Extreme = "extreme"


class ThunderDistance(BaseModel):
    """Indicator of distance for /thunder endpoint.
    """

    category: Distance = Distance.Extreme


@router.post("/thunder")
async def thunder(request: Request, distance: ThunderDistance = None):
    """Broadcast an ambient message to all chat room users.
    """
    wsp = request.get("room")
    if distance.category == Distance.Near:
        await wsp.broadcast_message("server", "Thunder booms overhead")
    elif distance == Distance.Far:
        await wsp.broadcast_message("server", "Thunder rumbles in the distance")
    else:
        await wsp.broadcast_message("server", "You feel a faint tremor")
    return {"broadcast": distance}


@router.websocket_route("/ws", name="ws")
class RoomLive(WebSocketEndpoint):
    """Live connection to the global :class:`~.Room` instance, via WebSocket.
    """

    encoding = "text"
    session_name = ""
    count = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = None
        self.user_id = None

    @classmethod
    def get_next_user_id(cls):
        """Returns monotonically increasing numbered usernames in the form
            'user_[number]'
        """
        user_id = f"user_{cls.count}"
        cls.count += 1
        return user_id

    async def on_connect(self, websocket):
        """Handle a new connection.
        New users are assigned a user ID and notified of the room's connected
        users. The other connected users are notified of the new user's arrival,
        and finally the new user is added to the global :class:`~.Room` instance.
        """
        room = self.scope.get("room")
        if room is None:
            raise RuntimeError(f"Global `Room` instance unavailable!")
        self.room = room
        self.user_id = self.get_next_user_id()
        await websocket.accept()
        await websocket.send_json(
            {"type": "ROOM_JOIN", "data": {"user_id": self.user_id}}
        )
        await self.room.broadcast_user_joined(self.user_id)
        self.room.add_user(self.user_id, websocket)

    async def on_disconnect(self, _websocket: WebSocket, _close_code: int):
        """Disconnect the user, removing them from the :class:`~.Room`, and
        notifying the other users of their departure.
        """
        self.room.remove_user(self.user_id)
        await self.room.broadcast_user_left(self.user_id)

    async def on_receive(self, _websocket: WebSocket, msg: str):
        """Handle incoming message: `msg` is forwarded straight to `broadcast_message`.
        """
        await self.room.broadcast_message(self.user_id, msg)
