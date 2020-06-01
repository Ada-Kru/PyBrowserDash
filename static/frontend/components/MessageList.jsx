import React, { Component } from "react"

class MessageList extends Component {
    constructor(props) {
        super(props)
        this.state = {
            unseenMessages: this.props.unseenMessages,
            updatedUnseen: this.props.updatedUnseen,
        }
    }

    componentDidUpdate = (prevProps) => {
        if (prevProps.updatedUnseen != this.props.updatedUnseen) {
            this.setState({
                unseenMessages: this.props.unseenMessages,
                updatedUnseen: this.props.updatedUnseen,
            })
        }
    }

    render() {
        let state = this.state
        return (
            <div id="MessageList">
                messages go here
            </div>
        )
    }
}

export default MessageList
