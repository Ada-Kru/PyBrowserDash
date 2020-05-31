import React, { Component } from "react"

class StatusBar extends Component {
    constructor(props) {
        super(props)
        this.state = {
            statusText: this.props.statusText,
            statusStyle: this.props.statusStyle,
            statusStats: this.props.statusStats,
        }
    }

    componentDidUpdate = (prevProps) => {
        if (prevProps.updatedStatsOnly != this.props.updatedStatsOnly) {
            this.setState({
                statusStats: this.props.statusStats,
            })
        } else if (
            prevProps.updatedStatusText != this.props.updatedStatusText
        ) {
            this.setState({
                statusText: this.props.statusText,
                statusStyle: this.props.statusStyle,
                statusStats: this.props.statusStats,
            })
        }
    }

    render() {
        let state = this.state
        return (
            <div id="statusBar">
                <span id="statusText" style={state.statusStyle}>
                    {state.statusText}
                </span>
                <span id="statusStats">{state.statusStats}</span>
            </div>
        )
    }
}

export default StatusBar
