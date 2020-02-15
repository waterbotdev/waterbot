import datetime
import json

from enum import Enum


class TimeHelper:
    '''Useful module for converting times and shit.
    '''

    @staticmethod
    def sec_to_str(sec):
        '''
        Convert Seconds to readable text format
        :param sec: Seconds
        :return:
        '''
        m = 0
        h = 0
        d = 0
        s = sec
        while s >= 86400:
            d += 1
            s -= 86400
            # print(f'Add D \tS:{s}\t{d}d\t{h}h\t{m}m\t{s}s', end='\r')
        while s >= 60 * 60:
            h += 1
            s -= 60 * 60
            # print(f'Add S \tS:{s}\t{d}d\t{h}h\t{m}m\t{s}s', end='\r')
        while s >= 60:
            m += 1
            s -= 60
            # print(f'Add M \tS:{s}\t{d}d\t{h}h\t{m}m\t{s}s', end='\r')
        return f'{d}d {h}h {m}m {s}s'


class DbS(Enum):
    MUTES = 'dbs/mutes.json'
    KICKS = 'dbs/kicks.json'
    BANS = 'dbs/bans.json'
    LOGS = 'dbs/logs.json'
    GUILDS = 'dbs/guild.json'


class DB:
    '''Database commands'''

    @staticmethod
    def addlog(uid: int, timestamp: int, item: str, description: str, modrid: int, end: int=None):
        '''
        Add a log object to the json database
        :param uid: User ID.
        :param timestamp: The timestamp that the item is recorded.
        :param item: The item that user infracted(mute, kick, ban, warn)
        :param description: Descriptions of the action, also includes different parameters, for specific types.
        :param modrid: Moderator responsible
        :param end:
        :return: None
        '''
        types = ['warn','mute','kick','tempban','ban']
        if item not in types:
            raise TypeError(f'Type {item} is not in the acceptable '
                            f'list.')
        file = open(DbS.LOGS.value, 'r')
        logs = json.load(file)
        file.close()
        if uid not in logs:
            logs[uid] = []
        logs[uid].append({
            "time": timestamp,
            "cate": item,
            "desc": {},
            "modr": modrid
        })
        logs[uid][len(logs[uid]) - 1]['desc']['reason'] = description
        if item == 'mute':
            if end is None:
                raise TypeError('"end" parameter does not have a value when using "mute" type')
            logs[uid][len(logs[uid])-1]['desc']['start'] = timestamp
            logs[uid][len(logs[uid])-1]['desc']['end'] = timestamp + end
        elif item == 'tempban':
            logs[uid][len(logs[uid]-1)]['desc']['start'] = timestamp
            logs[uid][len(logs[uid]) - 1]['desc']['end'] = timestamp + end


    @staticmethod
    def addmute(uid: int, seconds: int, reason: str):
        '''
        Add a mute record for a user
        :param uid: User ID
        :param seconds: Seconds for the mute(either calculated by hand/code or by TimeHelper.tosec()
        :param reason: Reason to be muted
        :return:None
        '''
        file = open(DbS.MUTES.value, 'r')
        mutes = json.load(file)
        mutes['uid'] = datetime.datetime.now().timestamp() + seconds

