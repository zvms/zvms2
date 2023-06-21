import Toast, { useToast, POSITION } from "vue-toastification";
import "vue-toastification/dist/index.css";

const defaultOptions = {
  position: POSITION.BOTTOM_RIGHT,
  draggable: true,
  draggablePercent: 0.1,
  showCloseButtonOnHover: true,
  hideProgressBar: true,
};

export const toasts = {
  success(message: string) {
    useToast().success(message, {
      ...defaultOptions,
      timeout: 2000,
      icon: {
        icon: "mdi-check-outline",
      },
    });
  },
  error(message: string) {
    useToast().error(message, {
      ...defaultOptions,
      timeout: 5000,
      icon: {
        icon: "mdi-close-outline",
      },
    });
  },
  warning(message: string) {
    useToast().warning(message, {
      ...defaultOptions,
      timeout: 3000,
      icon: {
        icon: "mdi-alert-outline",
      },
    });
  },
  info(message: string) {
    useToast().info(message, {
      ...defaultOptions,
      timeout: 2000,
      icon: {
        icon: "mdi-information-outline",
      },
    });
  },
  validateForm(isFormValid: boolean) {
    if (!isFormValid) {
      this.error("输入有误，请检查后重试");
    }
    return isFormValid;
  },
};

export default Toast;
