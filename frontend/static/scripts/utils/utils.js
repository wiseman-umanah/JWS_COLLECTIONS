export function email_validation (email) {
    const emailPattern = /^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$/;

    return emailPattern.test(email)
}
