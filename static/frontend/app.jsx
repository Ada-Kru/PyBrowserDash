import React, { Component } from "react";
import StatusBar from "./components/StatusBar";

const WS_DISCONNECTED = 0;
const WS_CONNECTING = 1;
const WS_CONNECTED = 2;
const STATUS_NORMAL_STYLE = { color: "white" };
const STATUS_ERROR_STYLE = { color: "red" };

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      wsState: WS_DISCONNECTED,
      statusText: "Backend disconnected",
      statusStyle: STATUS_ERROR_STYLE,
      statusStats: "",
      updatedStatusText: true,
      updatedStatsOnly: false,
    };
    this.ws = null;

    // Function maps for websocket events and internal events.
    this._wsMsgMap = {
      sys: this._onSystemInfoUpdate,
      backend: this._onBackendUpdate,
      music: this._onMusicPlayerUpdate,
      new_msg: this._onNewMessages,
      seen_msg: this._onSeenMessages,
      clear_all_msg: this._onClearAllMessages,
    };
  }

  _setupWebsocket = () => {
    this.ws = new WebSocket(
      `ws://${window.location.hostname}:${window.location.port}/`
    );
    this.setState({
      wsState: WS_CONNECTING,
    });
    this.setStatusText("Connecting...");

    this.ws.onopen = (evt) => {
      this.setState({
        wsState: WS_CONNECTED,
      });
      this.setStatusText("Connected");
    };

    this.ws.onmessage = (evt) => {
      let msg = JSON.parse(evt.data);
      // console.log(msg);
      for (let [type, data] of Object.entries(msg)) {
        if (this._wsMsgMap.hasOwnProperty(type)) {
          this._wsMsgMap[type](data);
        }
      }
    };

    this.ws.onclose = (evt) => {
      this.setState({
        wsState: WS_DISCONNECTED,
      });
      this.setStatusText("Backend disconnected", STATUS_ERROR_STYLE);
      setTimeout(() => this._setupWebsocket(), 1000);
    };

    this.ws.error = (evt) => {
      this.ws.close();
    };
  };

  _send = (data) => {
    this.ws.send(JSON.stringify(data))
  };

  _onSystemInfoUpdate = (update) => {
    this.setState({
      statusStats: update,
      updatedStatsOnly: !this.state.updatedStatsOnly,
    });
  };

  _onBackendUpdate = (update) => {
    console.log(update);
  };

  _onMusicPlayerUpdate = (update) => {
    console.log(update);
  };

  _onNewMessages = (update) => {
    console.log(update);
  };

  _onSeenMessages = (update) => {
    console.log(update);
  };

  _onClearAllMessages = (update) => {
    console.log(update);
  };

  componentDidMount = () => {
    this._setupWebsocket();
  };

  setStatusText = (text, style = null) => {
    this.setState({
      updatedStatusText: !this.state.updatedStatusText,
      statusText: text,
      statusStyle: style == null ? STATUS_NORMAL_STYLE : style,
    });
  };

  render() {
    let state = this.state;
    return (
      <div id="mainInteface">
        <div id="modules">
          <StatusBar
            updatedStatusText={state.updatedStatusText}
            updatedStatsOnly={state.updatedStatsOnly}
            statusText={state.statusText}
            statusStyle={state.statusStyle}
            statusStats={state.statusStats}
          ></StatusBar>
        </div>
      </div>
    );
  }
}

export default App;
