#!/usr/bin/python
# -*- coding: utf-8 -*-

def join(*args):
    return " ".join(list(args))

def execute_core(ansible, action, token=None):
    token_argument = join("--api-token", token) if token is not None else ""
    cmd = join(hassio, host, action, token_argument)
    return ansible.run_command(cmd)

def start(ansible, token):
    return execute_core(ansible, "start", token)

def restart(ansible, token):
    return execute_core(ansible, "restart", token)

def stop(ansible, token):
    return execute_core(ansible, "stop", token)

def update(ansible, token):
    return execute_core(ansible, "update", token)

def join(*args):
    return " ".join(list(args))

def update(ansible, token):
    cmd = join(hassio, host, "update", "--api-token", token)
    return ansible.run_command(cmd)

def __raise(ex):
    raise ex

def get_info(ansible, module, token=None):
    token_argument = join("--api-token ", token) if token is not None else ""
    cmd = join("ha ", module, " info --raw-json ", token_argument)
    return ansible.run_command(cmd)

def restart_requires_change(facts):
    return True #A restart always changes state

def update_requires_change(facts):
    return  facts["update_available"] is "true"

def stop_requires_change(facts):
    return True # There is currently no (unified) way to check whether services are actually running or not

def start_requires_change(facts):
    return True # There is currently no (unified) way to check whether services are actually running or not
    
state_and_changed= dict(restarted = restart_requires_change, updated = update_requires_change, stopped = stop_requires_change, started = start_requires_change)