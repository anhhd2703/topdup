import nodemailer from "nodemailer"
import smtpTransport  from "nodemailer-smtp-transport"
import {emailServer} from '../../configs/index'

console.log("EmailServer: ", emailServer)

let transporter = nodemailer.createTransport(smtpTransport({
    service: 'gmail',
    host: 'smtp.gmail.com',
    secure: true, // use SSL
    auth: {
        user: emailServer.user,
        pass: emailServer.pass
    }
}));
export default transporter
