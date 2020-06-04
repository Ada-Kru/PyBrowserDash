import React, { PureComponent } from "react"
import StatusBar from "./components/StatusBar"
import MusicBar from "./components/MusicBar"
import ControlBar from "./components/ControlBar"
import MessageList from "./components/MessageList"

const WS_DISCONNECTED = 0
const WS_CONNECTING = 1
const WS_CONNECTED = 2
const STATUS_NORMAL_STYLE = { color: "white" }
const STATUS_ERROR_STYLE = { color: "red" }
const STATS_NOT_LOADED_MSG = "System stats not loaded"
const WEATHER_NOT_LOADED = {
    display: "Weather info not loaded",
    tooltip: "Weather info not loaded",
}

class App extends PureComponent {
    constructor(props) {
        super(props)

        this.state = {
            wsState: WS_DISCONNECTED,
            statusText: "Backend disconnected",
            statusStyle: STATUS_ERROR_STYLE,
            statusWeather: WEATHER_NOT_LOADED,
            statusStats: STATS_NOT_LOADED_MSG,
            updatedStatusText: false,
            updatedStatsOnly: false,
            musicStatus: "disconnected",
            musicInfo: {},
            updatedMusic: false,
            backendMuted: false,
            unseenMessages: {},
            messageHistory: {},
            updatedUnseen: false,
        }
        this.ws = null
        this.musicActive = false
        this.numUnseen = 0
        this.numHistory = 0

        // Function maps for websocket events and internal events.
        this._wsMsgMap = {
            sys: this._onSystemInfoUpdate,
            weather: this._onWeatherUpdate,
            backend: this._onBackendUpdate,
            music: this._onMusicPlayerUpdate,
            new_msg: this._onNewMessages,
            seen: this._onSeenMessages,
            unseen: this._onUnseenMessages,
        }
    }

    _setupWebsocket = () => {
        this.ws = new WebSocket(
            `ws://${window.location.hostname}:${window.location.port}/`
        )
        this.setState({
            wsState: WS_CONNECTING,
        })
        this.setStatusText("Connecting...")

        this.ws.onopen = (evt) => {
            this.setState({
                wsState: WS_CONNECTED,
            })
            this.setStatusText("Connected")
        }

        this.ws.onmessage = (evt) => {
            let msg = JSON.parse(evt.data)
            // console.log(msg)
            for (let [type, data] of Object.entries(msg)) {
                if (this._wsMsgMap.hasOwnProperty(type)) {
                    this._wsMsgMap[type](data)
                }
            }
        }

        this.ws.onclose = (evt) => {
            this.setState({
                wsState: WS_DISCONNECTED,
                statusStats: STATS_NOT_LOADED_MSG,
                statusWeather: WEATHER_NOT_LOADED,
            })
            this.setStatusText("Backend disconnected", STATUS_ERROR_STYLE)
            setTimeout(() => this._setupWebsocket(), 1000)
        }

        this.ws.error = (evt) => {
            this.ws.close()
        }
    }

    _send = (data) => {
        this.ws.send(JSON.stringify(data))
    }

    _onSystemInfoUpdate = (update) => {
        this.setState({
            statusStats: update,
            updatedStatsOnly: !this.state.updatedStatsOnly,
        })
    }

    _onWeatherUpdate = (update) => {
        this.setState({
            statusWeather: update,
            updatedStatusText: !this.state.updatedStatusText,
        })
    }

    _onBackendUpdate = (update) => {
        this.setState({ backendMuted: update.muted })
    }

    _onMusicPlayerUpdate = (update) => {
        this.musicActive =
            update.player_state == "playing" || update.player_state == "paused"
        this.setState({
            musicStatus: update.player_state,
            musicInfo: update.active_item,
            updatedMusic: !this.state.updatedMusic,
        })
    }

    _onNewMessages = (update) => {
        let state = this.state
        Object.assign(state.unseenMessages, update)
        this.numUnseen = Object.keys(state.unseenMessages).length
        this.numHistory = 0
        this.setState({
            updatedUnseen: !state.updatedUnseen,
            messageHistory: {},
        })
    }

    _onSeenMessages = (update) => {
        let state = this.state
        for (let seen of update) {
            if (state.unseenMessages.hasOwnProperty(seen)) {
                delete state.unseenMessages[seen]
            }
        }
        this.numUnseen = Object.keys(state.unseenMessages).length
        this.setState({ updatedUnseen: !state.updatedUnseen })
    }

    _onUnseenMessages = (update) => {
        this.numUnseen = Object.keys(update).length
        this.numHistory = 0
        this.setState({
            unseenMessages: update,
            updatedUnseen: !this.state.updatedUnseen,
            messageHistory: {},
        })
    }

    _toggleMute = () => {
        if ((this.state.wsState = WS_CONNECTED)) {
            this.ws.send(JSON.stringify({ toggle_mute: true }))
        }
    }

    _messageButtonClick = () => {
        let state = this.state
        if (this.numHistory) {
            this.numHistory = 0
            this.setState({ messageHistory: {} })
        } else if (this.numUnseen) {
            fetch("messages/unseen/clear/", { method: "POST" })
        } else {
            fetch("messages/history/100/")
                .then((response) => response.text())
                .then(
                    (data) => {
                        data = JSON.parse(data)
                        this.numHistory = Object.keys(data.messages).length
                        this.setState({ messageHistory: data.messages })
                    },
                    (err) => {
                        console.log(err)
                    }
                )
        }
    }

    componentDidMount = () => {
        this._setupWebsocket()
    }

    setStatusText = (text, style = null) => {
        this.setState({
            updatedStatusText: !this.state.updatedStatusText,
            statusText: text,
            statusStyle: style == null ? STATUS_NORMAL_STYLE : style,
        })
    }

    render() {
        let state = this.state
        let msgs = this.numUnseen ? state.unseenMessages : state.messageHistory
        return (
            <div id="mainInterface">
                <div id="modules">
                    <ControlBar
                        backendMuted={state.backendMuted}
                        displayed={this.numUnseen || this.numHistory}
                        toggleMute={this._toggleMute}
                        messageButtonClick={this._messageButtonClick}
                    ></ControlBar>
                    {this.numUnseen || this.numHistory ? (
                        <MessageList
                            messages={msgs}
                            updatedUnseen={state.updatedUnseen}
                        ></MessageList>
                    ) : null}
                    {this.musicActive ? (
                        <MusicBar
                            updatedMusic={state.updatedMusic}
                            musicStatus={state.musicStatus}
                            musicInfo={state.musicInfo}
                        ></MusicBar>
                    ) : null}
                    <StatusBar
                        updatedStatusText={state.updatedStatusText}
                        updatedStatsOnly={state.updatedStatsOnly}
                        statusText={state.statusText}
                        statusStyle={state.statusStyle}
                        weatherDisplay={state.statusWeather.display}
                        weatherTooltip={state.statusWeather.tooltip}
                        statusStats={state.statusStats}
                    ></StatusBar>
                </div>
            </div>
        )
    }
}

export default App
