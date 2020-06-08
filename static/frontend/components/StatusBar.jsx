import React, { PureComponent } from "react"

class StatusBar extends PureComponent {
    constructor(props) {
        super(props)
        this.state = {
            statusText: this.props.statusText,
            statusStyle: this.props.statusStyle,
            statusStats: this.props.statusStats,
            weatherData: this.props.weatherData,
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
                weatherData: this.props.weatherData,
            })
        }
    }

    makeWeatherSpan = () => {
        if (this.state.weatherData.loaded == false) {
            return "Weather data not loaded."
        }

        let w = this.state.weatherData
        let temp = w.temp == null ? "-" : convertTemp(w.temp)
        let tempClass = "tempNormal"
        if (w.temp != null) {
            if (temp >= 85) {
                tempClass = "tempHot"
            } else if (temp <= 63) {
                tempClass = "tempCold"
            }
        }
        let wspd = w.wind_speed == null ? 0 : parseInt(w.wind_speed * 2.237)
        let wdir = degToDir(w.wind_dir)
        let gust = w.wind_gust == null ? 0 : parseInt(w.wind_gust * 2.237)
        return (
            <span>
                <span className={tempClass}>{`${temp}°F`}</span>
                {` ▬ ${wspd}${gust ? "-" + gust : ""} Mph ${wdir} ▬ ${w.desc}`}
            </span>
        )
    }

    makeWeatherTooltip = () => {
        if (this.state.weatherData.loaded == false) {
            return "Weather data not loaded."
        }

        let w = this.state.weatherData
        let press = w.pressure
        // let heat = w.heat == null ? "-" : `${convertTemp(w.heat)}`
        // let chill = w.chill == null ? "-" : `${convertTemp(w.chill)}`
        // let pres = w.pressure == null ? "-" : `${parseInt(w.pressure / 100)}`
        // let hum = w.humidity == null ? "-" : `${parseInt(w.humidity)}`
        return (
            `Last Updated: ${w.last_update}\n` +
            (w.heat == null ? "" : `Heat Index: ${convertTemp(w.heat)}\n`) +
            (w.chill == null ? "" : `Wind Chill: ${convertTemp(w.chill)}\n`) +
            (press == null ? "" : `Pressure: ${parseInt(press / 100)}\n`) +
            (w.humidity == null ? "" : `Humidity: ${parseInt(w.humidity)}`)
        )
    }

    render() {
        let state = this.state
        return (
            <div id="statusBar">
                <span id="statusText" style={state.statusStyle}>
                    {state.statusText}
                </span>
                <div className="statusSpansHolder">
                    <span id="statusWeather" title={this.makeWeatherTooltip()}>
                        {this.makeWeatherSpan()}
                    </span>
                    <span id="statusStats">{state.statusStats}</span>
                </div>
            </div>
        )
    }
}

function convertTemp(temp) {
    return parseInt(celToFarn(temp))
}

function celToFarn(temp) {
    return (9 / 5) * temp + 32
}

function degToDir(degrees) {
    if (degrees == null || degrees < 22.5) return "N"
    else if (degrees < 67.5) return "NE"
    else if (degrees < 112.5) return "E"
    else if (degrees < 157.5) return "SE"
    else if (degrees < 202.5) return "S"
    else if (degrees < 247.5) return "SW"
    else if (degrees < 292.5) return "W"
    else if (degrees < 337.5) return "NW"
    else return "N"
}

export default StatusBar
