def delta_check(characteristic, initial, final, expected_delta, tol=0):
    delta = final - initial
    min_ = expected_delta - tol
    max_ = expected_delta + tol
    condition = (min_ <= delta <= max_)
    pass_msg = "%s Delta (%s) within expected limits: %s +/- %s" % (characteristic, delta, expected_delta, tol)
    fail_msg = "%s Delta (%s) OUTSIDE expected limits: %s +/- %s" % (characteristic, delta, expected_delta, tol)
    return {'condition': condition, 'pass_msg': pass_msg, 'fail_msg': fail_msg}
