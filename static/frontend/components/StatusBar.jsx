import React, { PureComponent } from "react"

class StatusBar extends PureComponent {
    constructor(props) {
        super(props)
        this.state = {
            statusText: this.props.statusText,
            statusStyle: this.props.statusStyle,
            weatherDisplay: this.props.weatherDisplay,
            weatherTooltip: this.props.weatherTooltip,
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
                weatherDisplay: this.props.weatherDisplay,
                weatherTooltip: this.props.weatherTooltip,
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
                <div className="statusSpansHolder">
                    <span id="statusWeather" title={state.weatherTooltip}>
                        {state.weatherDisplay}
                    </span>
                    <span id="statusStats">{state.statusStats}</span>
                </div>
            </div>
        )
    }
}

export default StatusBar
