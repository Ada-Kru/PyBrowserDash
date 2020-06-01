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
                    {state.displayed ? "Close Messages" : "Show History"}
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
