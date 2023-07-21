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

def __raise(ex):
    raise ex

def get_info(ansible, module, token=None):
    token_argument = join("--api-token ", token) if token is not None else ""
    cmd = join("ha ", module, " info --raw-json ", token_argument)
    return ansible.run_command(cmd)
