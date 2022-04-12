import React, { PureComponent } from "react"

class MusicBar extends PureComponent {
    constructor(props) {
        super(props)
        let info = this.props.musicInfo
        this.state = {
            updatedMusic: this.props.updatedMusic,
            musicStatus: this.props.musicStatus,
            artist: info.artist,
            album: info.album,
            title: info.title,
            length: info.length,
            position: info.position,
            positionDisplay: this.secondsToHHMMSS(info.position),
            lengthDisplay: this.secondsToHHMMSS(info.length),
        }

        this.timer = null
        this.setupProgress()
    }

    componentDidUpdate = (prevProps) => {
        if (prevProps.updatedMusic != this.props.updatedMusic) {
            let info = this.props.musicInfo
            this.setState(
                {
                    updatedMusic: this.props.updatedMusic,
                    musicStatus: this.props.musicStatus,
                    artist: info.artist,
                    album: info.album,
                    title: info.title,
                    length: info.length,
                    position: info.position,
                    positionDisplay: this.secondsToHHMMSS(info.position),
                    lengthDisplay: this.secondsToHHMMSS(info.length),
                },
                this.setupProgress
            )
        }
    }

    secondsToHHMMSS = (ttlSecs) => {
        let hours = parseInt(ttlSecs / 3600)
        let minutes = parseInt((ttlSecs - hours * 3600) / 60)
        let seconds = Math.floor(ttlSecs - (hours * 3600 + minutes * 60))
        return (
            (hours < 10 ? "0" + hours : hours) +
            ":" +
            (minutes < 10 ? "0" + minutes : minutes) +
            ":" +
            (seconds < 10 ? "0" + seconds : seconds)
        )
    }

    clearTimer = () => {
        if (this.timer != null) {
            clearInterval(this.timer)
            this.timer = null
        }
    }

    updateProgress = () => {
        let newPos = this.state.position + 1
        if (newPos > this.state.length) {
            this.clearTimer()
            return
        }
        this.setState({
            position: newPos,
            positionDisplay: this.secondsToHHMMSS(newPos),
        })
    }

    setupProgress = () => {
        this.clearTimer()
        if (this.state.musicStatus == "playing") {
            this.timer = setInterval(this.updateProgress, 1000)
        }
    }

    makeTitle = () => {
        let state = this.state
        if (state.musicStatus != "paused") {
            return `${state.artist} - ${state.album} - ${state.title}`
        } else {
            return `(PAUSED) ${state.artist} - ${state.album} - ${state.title} (PAUSED)`
        }
    }

    componentWillUnmount = () => {
        this.clearTimer()
    }

    render() {
        let state = this.state
        return (
            <div id="musicBar">
                <span id="musicCurrentTime" className="musicTimes">
                    {state.positionDisplay}
                </span>
                <progress
                    id="musicProgressBar"
                    className="greenProgressBar"
                    value={state.position}
                    max={state.length}
                ></progress>
                <span id="musicTitle">{this.makeTitle()}</span>
                <span id="musicTotalTime" className="musicTimes">
                    {state.lengthDisplay}
                </span>
            </div>
        )
    }
}

export default MusicBar
