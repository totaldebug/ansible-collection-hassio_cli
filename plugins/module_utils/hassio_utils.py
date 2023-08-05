#!/usr/bin/python
# -*- coding: utf-8 -*-

hassio = "ha"


def join(*args):
    return " ".join(list(args))


def execute(ansible, module, action, token=None):
    token_argument = join("--api-token", token) if token is not None else ""
    cmd = join(hassio, module, action, token_argument)
    return ansible.run_command(cmd)


def start(module, ansible, token=None):
    return execute(ansible, module, "start", token)


def restart(module, ansible, token=None):
    return execute(ansible, module, "restart", token)


def stop(module, ansible, token=None):
    return execute(ansible, module, "stop", token)


def update(module, ansible, token=None):
    return execute(ansible, module, "update", token)


def __raise(ex):
    raise ex

def get_info(ansible, module, token=None):
    token_argument = join("--api-token ", token) if token is not None else ""
    cmd = join("ha ", module, " info --raw-json ", token_argument)
    return ansible.run_command(cmd)

def restart_requires_change(facts):
    return True #A restart always changes state

def update_requires_change(facts):
    return  facts["update_available"] is True

def stop_requires_change(facts):
    return True # There is currently no (unified) way to check whether services are actually running or not

def start_requires_change(facts):
    return True # There is currently no (unified) way to check whether services are actually running or not
    
state_and_changed= dict(restarted = restart_requires_change, updated = update_requires_change, stopped = stop_requires_change, started = start_requires_change)