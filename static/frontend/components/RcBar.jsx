import React, { PureComponent } from "react"

class RcBar extends PureComponent {
    constructor(props) {
        super(props)
        this.state = {
            emitters: [0]
        };
    }

    handleBtnClick = (evt) => {

        const cmd = evt.target.dataset.cmd;
        this.props.onSendCommand(cmd, this.state.emitters);
    };

    handleSelectEmitter = (evt) => {

        const newEmitters = [...this.state.emitters];
        const emitterNum = parseInt(evt.target.value);
        const index = newEmitters.indexOf(emitterNum);
        if (!evt.target.checked) {
            if (index != -1) {
                newEmitters.splice(index, 1);
            }
        }
        else if (index === -1) {
            newEmitters.push(emitterNum);
        }

        if (newEmitters.length) {
            this.setState({ emitters: newEmitters });
        }
    };

    render() {
        let state = this.state

        return (
            <div id="rcBar">
                <button id="rcFav1" data-cmd="21" className="controlButton" onClick={this.handleBtnClick}>
                    Fav 1
                </button>
                <button id="rcFav2" data-cmd="23" className="controlButton" onClick={this.handleBtnClick}>
                    Fav 2
                </button>
                <button id="rcFav3" data-cmd="18" className="controlButton" onClick={this.handleBtnClick}>
                    Fav 3
                </button>
                <button id="rcFav4" data-cmd="22" className="controlButton" onClick={this.handleBtnClick}>
                    Fav 4
                </button>
                <button id="rcFav5" data-cmd="77" className="controlButton" onClick={this.handleBtnClick}>
                    Fav 5
                </button>
                <button id="moreRed" data-cmd="76" className="controlButton" onClick={this.handleBtnClick}>
                    Red +
                </button>
                <button id="rcMoreYellow" data-cmd="14" className="controlButton" onClick={this.handleBtnClick}>
                    Yellow +
                </button>
                <button id="rcMoreGreen" data-cmd="20" className="controlButton" onClick={this.handleBtnClick}>
                    Green +
                </button>
                <button id="rcMorePurple" data-cmd="10" className="controlButton" onClick={this.handleBtnClick}>
                    Purple +
                </button>
                <button id="rcRed" data-cmd="25" className="controlButton" onClick={this.handleBtnClick}>
                    Red
                </button>
                <button id="rcGreen" data-cmd="27" className="controlButton" onClick={this.handleBtnClick}>
                    Green
                </button>
                <button id="rcBlue" data-cmd="17" className="controlButton" onClick={this.handleBtnClick}>
                    Blue
                </button>
                <button id="rcWarm" data-cmd="09" className="controlButton" onClick={this.handleBtnClick}>
                    Warm White
                </button>
                <button id="rcNeutral" data-cmd="29" className="controlButton" onClick={this.handleBtnClick}>
                    Neutral White
                </button>
                <button id="rcCold" data-cmd="31" className="controlButton" onClick={this.handleBtnClick}>
                    Cold White
                </button>
                <button id="rcBright" data-cmd="01" className="controlButton" onClick={this.handleBtnClick}>
                    Brighten
                </button>
                <button id="rcDim" data-cmd="16" className="controlButton" onClick={this.handleBtnClick}>
                    Dim
                </button>
                <button id="rcOff" data-cmd="06" className="controlButton" onClick={this.handleBtnClick}>
                    Off
                </button>
                <button id="rcOn" data-cmd="13" className="controlButton" onClick={this.handleBtnClick}>
                    On
                </button>

                <input
                    type="checkbox"
                    id="emitterEastCheckbox"
                    name="emitterEast"
                    onChange={this.handleSelectEmitter}
                    checked={state.emitters.includes(0)}
                    value="0" 
                />
                <label htmlFor="emitterEastCheckbox">East</label>

                <input
                    type="checkbox"
                    id="emitterNorthCheckbox"
                    name="emitterNorth"
                    onChange={this.handleSelectEmitter}
                    checked={state.emitters.includes(1)}
                    value="1" 
                />
                <label htmlFor="emitterNorthCheckbox">North</label>
            </div>
        )
    }
}

export default RcBar
