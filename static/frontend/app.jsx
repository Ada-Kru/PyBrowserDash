import React, { Component } from "react"

class App extends Component {
    constructor(props) {
        super(props)

        this.state = { wsState: "disconnected" }
        this.ws = null

        // Function maps for websocket events and internal events.
        // this._wsMsgMap = {
        //     point_update: this.onMsgPointUpdate,
        //     category_added: this.onAddedBackendCat,
        //     category_removed: this.onRemovedBackendCat,
        //     removed_points: this.onBackendRemovedPoints,
        // }
    }

    setupWebsocket = () => {
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
            // for (let [type, data] of Object.entries(msg)) {
            //     if (this._wsMsgMap.hasOwnProperty(type)) {
            //         this._wsMsgMap[type](data)
            //     }
            // }
        }

        this.ws.onclose = (evt) => {
            this.setState({ wsState: "disconnected" })
            setTimeout(() => this.setupWebsocket(), 1000)
        }

        this.ws.error = evt => {
            this.ws.close()
        }
    }

    _send = data => {
        this.ws.send(JSON.stringify(data))
    }

    componentDidMount() {
        this.setupWebsocket()
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
