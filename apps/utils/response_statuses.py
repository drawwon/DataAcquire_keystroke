RESPONSE_STATUS = {
    'SUCCESS': 'success',
    'NEED_MORE_SAMPLE': 'need_more_sample',
    'ERROR': 'error',
    'REQUEST_ERROR': 'request_error',
    'INVALID_KEYSTROKE': 'invalid_keystroke',
}

RESPONSE = {
    'NEED_MORE_SAMPLE': {
        'status': RESPONSE_STATUS['NEED_MORE_SAMPLE'],
        'message': 'Please, fill the field again. We need more samples to create your keystroke signature',
    },
    'SUCCESS': {
        'status': RESPONSE_STATUS['SUCCESS'],
        # 'message': 'Your keystroke was successfully created',
        'message': 'Your keystroke was successfully stored',
    },
    'INVALID_KEYSTROKE': {
        'status': RESPONSE_STATUS['INVALID_KEYSTROKE'],
        'message': 'Time intervals of typing are significantly out of norm. Please, try again.'
    }
}
