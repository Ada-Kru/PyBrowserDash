import React, { PureComponent } from "react"

class ControlBar extends PureComponent {
    constructor(props) {
        super(props)
        this.state = {
            backendMuted: this.props.backendMuted,
            displayed: this.props.displayed,
        }
    }

    componentDidUpdate = (prevProps) => {
        if (
            prevProps.backendMuted != this.props.backendMuted ||
            prevProps.displayed != this.props.displayed
        ) {
            this.setState({
                backendMuted: this.props.backendMuted,
                displayed: this.props.displayed,
            })
        }
    }

    render() {
        let state = this.state
        return (
            <div id="controlBar">
                <button
                    id="messagesButton"
                    className="controlButton"
                    onClick={this.props.messageButtonClick}
                >
                    {state.displayed ? "Close Messages" : "History"}
                </button>
                <span className="controlSpacer"></span>
                <button
                    id="muteButton"
                    className={
                        "controlButton" +
                        (state.backendMuted ? " activated" : "")
                    }
                    onClick={this.props.toggleMute}
                >
                    {state.backendMuted ? "Unmute" : "Mute"}
                </button>
                <button id="rcToggleButton" className="controlButton" onClick={this.props.toggleRcBar}>Remote</button>
            </div>
        )
    }
}

export default ControlBar
