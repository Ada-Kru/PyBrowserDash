import React, { PureComponent } from "react"

class RcBar extends PureComponent {
    constructor(props) {
        super(props)
        this.state = {
            emitters: [1, 2]
        };
    }

    handleClick = (evt) => {

        const cmd = evt.target.dataset.cmd;
        this.props.onSendCommand(cmd, this.state.emitters);
    }

    render() {
        let state = this.state
        return (
            <div id="rcBar">
                <button id="rcFav1" data-cmd="21" className="controlButton" onClick={this.handleClick}>Fav 1</button>
                <button id="rcFav2" data-cmd="23" className="controlButton" onClick={this.handleClick}>Fav 2</button>
                <button id="rcFav3" data-cmd="18" className="controlButton" onClick={this.handleClick}>Fav 3</button>
                <button id="rcFav4" data-cmd="22" className="controlButton" onClick={this.handleClick}>Fav 4</button>
                <button id="rcFav5" data-cmd="77" className="controlButton" onClick={this.handleClick}>Fav 5</button>
                <button id="moreRed" data-cmd="76" className="controlButton" onClick={this.handleClick}>
                    Red +
                </button>
                <button id="rcMoreYellow" data-cmd="14" className="controlButton" onClick={this.handleClick}>
                    Yellow +
                </button>
                <button id="rcMoreGreen" data-cmd="20" className="controlButton" onClick={this.handleClick}>
                    Green +
                </button>
                <button id="rcMorePurple" data-cmd="10" className="controlButton" onClick={this.handleClick}>
                    Purple +
                </button>
                <button id="rcRed" data-cmd="25" className="controlButton" onClick={this.handleClick}>
                    Red
                </button>
                <button id="rcGreen" data-cmd="27" className="controlButton" onClick={this.handleClick}>
                    Green
                </button>
                <button id="rcBlue" data-cmd="17" className="controlButton" onClick={this.handleClick}>
                    Blue
                </button>
                <button id="rcWarm" data-cmd="09" className="controlButton" onClick={this.handleClick}>
                    Warm White
                </button>
                <button id="rcNeutral" data-cmd="29" className="controlButton" onClick={this.handleClick}>
                    Neutral White
                </button>
                <button id="rcCold" data-cmd="31" className="controlButton" onClick={this.handleClick}>
                    Cold White
                </button>
                <button id="rcBright" data-cmd="01" className="controlButton" onClick={this.handleClick}>
                    Brighten
                </button>
                <button id="rcDim" data-cmd="16" className="controlButton" onClick={this.handleClick}>
                    Dim
                </button>
                <button id="rcOff" data-cmd="06" className="controlButton" onClick={this.handleClick}>
                    Off
                </button>
                <button id="rcOn" data-cmd="13" className="controlButton" onClick={this.handleClick}>
                    On
                </button>
            </div>
        )
    }
}

export default RcBar
