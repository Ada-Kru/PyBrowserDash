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
        let msgs = state.unseenMessages
        return (
            <div id="messageList">
                <table id="msgTable">
                    <thead id="msgTableHeaders">
                        <tr className="msgHeaderRow">
                            <th className="msgHeader timeCol">Time</th>
                            <th className="msgHeader senderCol">Sender</th>
                            <th className="msgHeader msgCol">Message</th>
                        </tr>
                    </thead>
                    <tbody id="msgTableBody">
                        {Object.keys(msgs).map((key) => {
                            let m = msgs[key]
                            return (
                                <tr
                                    key={key}
                                    className={`msgRow ${m.class_name}`}
                                >
                                    <td className="timeCol">{m.time}</td>
                                    <td className="senderCol">{m.sender}</td>
                                    <td className="msgCol">{m.text}</td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>
        )
    }
}

export default MessageList
