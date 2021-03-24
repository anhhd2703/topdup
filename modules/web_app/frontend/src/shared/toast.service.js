import { toast } from 'react-toastify'
import { Severity } from './constants'

export class ToastService {
  toastDisplayOption = {
    position: "bottom-right",
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    progress: undefined,
  }

  displayToast = (_reponse, severity) => {
    const reponse = _reponse || {}
    const resContent = reponse.data || {}
    const message = resContent.message || reponse.message
    switch (severity) {
      case Severity.Success:
        toast.success('✔️ ' + message, this.toastDisplayOption)
        break
      case Severity.Warning:
        toast.warning('⚠️ ' + message, this.toastDisplayOption)
        break
      case Severity.Error:
        toast.error('❌ ' + message, this.toastDisplayOption)
        break
      default:
        toast.info(message, this.toastDisplayOption)
        break
    }
  }
}