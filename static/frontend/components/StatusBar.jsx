import React, { PureComponent } from "react"
import moment from "moment-mini"

const SYS_STATS_NOT_LOADED_MSG = "System stats not loaded."
const DATE_FORMAT = "ddd D, H:mm"

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
            return (
                <span id="statusWeather" title={this.makeWeatherTooltip()}>
                    "Weather data not loaded."
                </span>
            )
        }

        let w = this.state.weatherData
        let temp = w.temp == null ? "-" : convertTemp(w.temp)
        let tempClass = "statNormal"
        if (w.temp != null) {
            if (temp >= 85) {
                tempClass = "statHigh"
            } else if (temp <= 63) {
                tempClass = "statLow"
            }
        }
        let gust = w.wind_gust == null ? 0 : parseInt(w.wind_gust * 0.621371)
        let wspd = w.wind_speed == null ? 0 : parseInt(w.wind_speed * 0.621371)
        if (w.wind_speed == null && w.wind_gust != null) {
            wspd = Math.max(wspd, parseInt(gust / 2))
        }
        let wdir = degToDir(w.wind_dir)
        let dataTime = moment(w.last_updated)
        let startTime = moment().subtract(1.5, "hours")
        let isOldData = dataTime.isSameOrBefore(startTime) ? " 🕓" : ""
        return (
            <span id="statusWeather" title={this.makeWeatherTooltip()}>
                <span className={tempClass}>{`${temp}°F`}</span>
                {` ▬ ${wspd}${gust ? "-" + gust : ""} Mph ` +
                    `${wdir} ▬ ${w.desc}${isOldData}`}
            </span>
        )
    }

    makeWeatherTooltip = () => {
        if (this.state.weatherData.loaded == false) {
            return "Weather data not loaded."
        }

        let w = this.state.weatherData
        let press = w.pressure
        return (
            `Retrieved at: ${w.retrieved_time}\n` +
            `Data timestamp: ${moment(w.last_updated).format(DATE_FORMAT)}\n` +
            (w.heat == null ? "" : `Heat Index: ${convertTemp(w.heat)}\n`) +
            (w.chill == null ? "" : `Wind Chill: ${convertTemp(w.chill)}\n`) +
            (press == null ? "" : `Pressure: ${parseInt(press / 100)}\n`) +
            (w.humidity == null ? "" : `Humidity: ${parseInt(w.humidity)}`)
        )
    }

    makeSystemStats = () => {
        let stats = this.state.statusStats
        if (stats.cpu == null) {
            return <span id="statusStats">{SYS_STATS_NOT_LOADED_MSG}</span>
        }

        let cpuClass = ""
        if (stats.cpu >= 75) {
            cpuClass = "statRed"
        } else if (stats.cpu >= 25) {
            cpuClass = "statHigh"
        }

        let ramClass = ""
        let ramPct = (stats.ram_used / stats.ram_total) * 100
        if (ramPct >= 75) {
            ramClass = "statRed"
        } else if (ramPct >= 50) {
            ramClass = "statHigh"
        }

        let n = stats.net

        return (
            <span id="statusStats">
                CPU:
                <span className={cpuClass}>
                    {("     " + stats.cpu).slice(-4)}
                </span>
                % RAM:{" "}
                <span className={ramClass}>{stats.ram_used.toFixed(1)}</span>G
                ▬▬ NET: {n <= 99999 ? ("     " + n).slice(-5) : n}K
            </span>
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
                    {this.makeWeatherSpan()}
                    {this.makeSystemStats()}
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
