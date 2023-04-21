import { toasts } from "./dialogs";

/**
 * If one of `vars` is `NAN`, open a dialog.
 * @param  {...string} vars
 * @returns `true` if one of `vars` is `NAN`
 */
export function validateNotNAN(
  msg = "就连幼儿园的小孩子都知道，时间得是数字！！！"
) {
  return (...vars: any[]) => {
    if (vars.findIndex((v) => isNaN(parseInt(v))) !== -1) {
      toasts.error(msg);
      return true;
    } else {
      return false;
    }
  };
}

export function validateNotNegative(
  msg = "就连幼儿园的小孩子都知道，不能是负数！！！"
) {
  return (...vars: any[]) => {
    if (vars.findIndex((v) => v < 0) !== -1) {
      toasts.error(msg);
      return true;
    } else {
      return false;
    }
  };
}

export function validateNotLargerThan(
  max: number,
  msg = "就连幼儿园的小孩子都知道，你这数字有点大！！！"
) {
  return (...vars: any[]) => {
    if (vars.findIndex((v) => v > max) !== -1) {
      toasts.error(msg);
      return true;
    } else {
      return false;
    }
  };
}

/**
 * @returns the index number of validator that fails. `-1` if none fails.
 */
export function validate(
  vars: any,
  validators: ((...any: any[]) => boolean)[]
) {
  for (const i in validators) {
    const validator = validators[i];
    if (!validator(...vars)) return i;
  }
  return -1;
}

export const NOT_EMPTY = () => (v: any) => !!v || "此处不能为空";
export const IS_NUMBER = () => (v: any) => !isNaN(parseFloat(v)) || "此处必须填数字";
export const IS_DECIMAL = () => (v: any) => !isNaN(parseInt(v)) || "此处必须填整数";
export const NOT_NEGATIVE = () => (v: any) => parseFloat(v) >= 0 || "此处不能为负";
export const IS_POSITIVE = () => (v: any) => parseFloat(v) > 0 || "此处必须为正数";

/**
 * e.g. 22-9-1 10:30
 */
const TimeRegex = /^\d{1,4}-\d{1,2}-\d{1,2} +\d{1,2}[:：]\d{1,2}$/;
export const TIME = () => (v: any) => {
  return TimeRegex.test(v) || "格式不正确！";
};
