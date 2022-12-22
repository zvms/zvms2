import { toasts } from "./dialogs";

/**
 * If one of `vars` is `NAN`, open a dialog.
 * @param  {...string} vars 
 * @returns `true` if one of `vars` is `NAN`
 */
export function validateNotNAN(msg = "就连幼儿园的小孩子都知道，时间得是数字！！！") {
    return (...vars: any[]) => {
        if (vars.findIndex(v => isNaN(parseInt(v))) !== -1) {
            toasts.error(msg)
            return true;
        } else {
            return false;
        }
    }
}

export function validateNotNegative(msg = "就连幼儿园的小孩子都知道，不能是负数！！！") {
    return (...vars: any[]) => {
        if (vars.findIndex(v => v < 0) !== -1) {
            toasts.error(msg)
            return true;
        } else {
            return false;
        }
    }
}


export function validateNotLargerThan(max: number, msg = "就连幼儿园的小孩子都知道，你这数字有点大！！！") {
    return (...vars: any[]) => {
        if (vars.findIndex(v => v > max) !== -1) {
            toasts.error(msg)
            return true;
        } else {
            return false;
        }
    }
}

/**
 * @returns the index number of validator that fails. `-1` if none fails.
 */
export function validate(vars: any, validators: ((...any: any[]) => boolean)[]) {
    for (const i in validators) {
        const validator = validators[i];
        if (!validator(...vars))
            return i;
    }
    return -1;
}

export const NOTEMPTY = () => (v: any) => !!v || '此处不能为空'