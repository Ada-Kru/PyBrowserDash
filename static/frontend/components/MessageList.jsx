import React, { PureComponent } from "react"
import moment from "moment"

const DATE_FORMAT = "HH:mm:ss / MM-DD-YYYY"

class MessageList extends PureComponent {
    constructor(props) {
        super(props)
        this.state = {
            messages: this.props.messages,
            updatedUnseen: this.props.updatedUnseen,
        }
        this.tableEnd = React.createRef()
    }

    componentDidMount = () => {
        this.scrollToBottom()
    }

    componentDidUpdate = (prevProps) => {
        if (prevProps.updatedUnseen != this.props.updatedUnseen) {
            this.setState({
                messages: this.props.messages,
                updatedUnseen: this.props.updatedUnseen,
            })
        }
        this.scrollToBottom()
    }

    scrollToBottom = () => {
        this.tableEnd.current.scrollIntoView()
    }

    render() {
        let state = this.state
        let msgs = state.messages
        return (
            <div id="messageList">
                <table id="msgTable">
                    <thead id="msgTableHeaders">
                        <tr className="msgHeaderRow">
                            <th className="msgHeader seenCol">New</th>
                            <th className="msgHeader timeCol">Time</th>
                            <th className="msgHeader senderCol">Sender</th>
                            <th className="msgHeader msgCol">Message</th>
                        </tr>
                    </thead>
                    <tbody id="msgTableBody">
                        {Object.keys(msgs).map((key) => {
                            let m = msgs[key]
                            let seen = m.hasOwnProperty("seen") ? m.seen : true
                            let datetime = moment(m.time).format(DATE_FORMAT)
                            let rowClass = `msgRow ${m.class_name}`
                            return (
                                <tr key={key} className={rowClass}>
                                    <td className="seenCol">
                                        {seen ? "" : "✔️"}
                                    </td>
                                    <td className="timeCol">{datetime}</td>
                                    <td className="senderCol" title={m.sender}>
                                        {m.sender}
                                    </td>
                                    <td className="msgCol">{m.text}</td>
                                </tr>
                            )
                        })}
                        <div ref={this.tableEnd}></div>
                    </tbody>
                </table>
            </div>
        )
    }
}

export default MessageList
