import React, { Component } from "react"

class App extends Component {
    constructor(props) {
        super(props)

        this.state = { wsState: "disconnected" }
        this.ws = null

        // Function maps for websocket events and internal events.
        this._wsMsgMap = {
            sys: this._onSystemInfoUpdate,
            backend: this._onBackendUpdate,
            music: this._onMusicPlayerUpdate,
            new_msg: this._onNewMessages,
            seen_msg: this._onSeenMessages,
            clear_all_msg: this._onClearAllMessages,
        }
    }

    _setupWebsocket = () => {
        this.ws = new WebSocket(
            `ws://${window.location.hostname}:${window.location.port}/`
        )
        this.setState({ wsState: "connecting" })

        this.ws.onopen = evt => {
            this.setState({ wsState: "connected" })
        }

        this.ws.onmessage = evt => {
            let msg = JSON.parse(evt.data)
            console.log(msg)
            for (let [type, data] of Object.entries(msg)) {
                if (this._wsMsgMap.hasOwnProperty(type)) {
                    this._wsMsgMap[type](data)
                }
            }
        }

        this.ws.onclose = (evt) => {
            this.setState({ wsState: "disconnected" })
            setTimeout(() => this._setupWebsocket(), 1000)
        }

        this.ws.error = evt => {
            this.ws.close()
        }
    }

    _send = data => {
        this.ws.send(JSON.stringify(data))
    }

    _onSystemInfoUpdate = update => {
        console.log(update)
    }

    _onBackendUpdate = update => {
        console.log(update)
    }

    _onMusicPlayerUpdate = update => {
        console.log(update)
    }

    _onNewMessages = update => {
        console.log(update)
    }

    _onSeenMessages = update => {
        console.log(update)
    }

    _onClearAllMessages = update => {
        console.log(update)
    }

    componentDidMount() {
        this._setupWebsocket()
    }

    render() {
        return (
            <div>
                react loaded
            </div>
        )
    }
}

export default App
