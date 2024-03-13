```ts
declare interface SuccessResponse<T> {
    status: 'success'
    code: HTTP Status Code
    data: T
}

declare interface ErrorResponse {
    status: 'error',
    code: HTTP Status Code
    message: string // 错误信息
}
```
