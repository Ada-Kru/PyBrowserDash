import React, { Component } from "react"

class ControlBar extends Component {
    constructor(props) {
        super(props)
        this.state = {
            backendMuted: this.props.backendMuted,
        }
    }

    componentDidUpdate = (prevProps) => {
        if (prevProps.backendMuted != this.props.backendMuted) {
            this.setState({
                backendMuted: this.props.backendMuted,
            })
        }
    }

    render() {
        let state = this.state
        return (
            <div id="controlBar">
                <button id="logButton" className="controlButton">
                    Log
                </button>
                <button id="messagesButton" className="controlButton">
                    Messages
                </button>
                <span className="spacer"></span>
                <button
                    id="muteButton"
                    className={
                        "toggleButton" +
                        (state.backendMuted ? " activated" : "")
                    }
                    onClick={this.props.toggleMute}
                >
                    Mute
                </button>
            </div>
        )
    }
}

export default ControlBar
