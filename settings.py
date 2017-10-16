class Settings:
    def __init__(self, db):
        self.db = db

        self.hosts = [
            row['hostname']
            for row in db.load_table('settings').distinct('hostname')
        ]

        self.keys = [
            row['value']
            for row in db.load_table('settings').distinct('value')
        ]

        self.data = {}
        for host in self.hosts:
            self.data[host] = {}
            for key in self.keys:
                self.data[host][key] = None
        for row in db.load_table('settings'):
            host = row['hostname']
            key = row['value']
            value = row['data']
            self.data[host][key] = value

    def compare(self, host1, host2):
        for host in [host1, host2]:
            if host not in self.hosts:
                raise RuntimeError(f'Host {host} does not exist')

        only_host1 = []
        only_host2 = []
        matching = []
        different = []

        data1 = self.data[host1]
        data2 = self.data[host2]

        for key in self.keys:
            if data1[key] is not None and data2[key] is None:
                only_host1.append((key, data1[key]))
            elif data2[key] is not None and data1[key] is None:
                only_host2.append((key, data2[key]))
            else:
                if data1[key] == data2[key]:
                    matching.append((key, data1[key]))
                else:
                    different.append((key, data1[key], data2[key]))

        return (only_host1, only_host2, matching, different)

    def copy(self, from_host, to_host, copy_keys):
        for host in [from_host, to_host]:
            if host not in self.hosts:
                raise RuntimeError(f'Host {host} does not exist')

        table = self.db.load_table('settings')

        for key in copy_keys:
            if key not in self.keys:
                raise RuntimeError(f'Key {key} does not exist')
            if self.data[from_host][key] is None:
                raise RuntimeError(f'Cannot copy missing value for key {key}')

            if self.data[from_host][key] == self.data[to_host][key]:
                continue

            row = {
                'hostname': to_host,
                'value': key,
                'data': self.data[from_host][key],
            }

            table.upsert(row, keys = ['hostname', 'value'])
            self.data[to_host][key] = self.data[from_host][key]


class Bindings:
    def __init__(self, db):
        self.db = db

        self.hosts = [
            row['hostname']
            for row in db.load_table('keybindings').distinct('hostname')
        ]

        self.actions = [
            (row['context'], row['action'])
            for row in db.load_table('keybindings').distinct('context', 'action')
        ]

        self.data = {}
        for host in self.hosts:
            self.data[host] = {}
            for action in self.actions:
                self.data[host][action] = None
        for row in db.load_table('keybindings'):
            host = row['hostname']
            action = (row['context'], row['action'])
            keys = row['keylist']
            self.data[host][action] = keys

    def compare(self, host1, host2):
        for host in [host1, host2]:
            if host not in self.hosts:
                raise RuntimeError(f'Host {host} does not exist')

        only_host1 = []
        only_host2 = []
        matching = []
        different = []

        data1 = self.data[host1]
        data2 = self.data[host2]

        for action in self.actions:
            if data1[action] is not None and data2[action] is None:
                only_host1.append((action, data1[action]))
            elif data2[action] is not None and data1[action] is None:
                only_host2.append((action, data2[action]))
            else:
                if data1[action] == data2[action]:
                    matching.append((action, data1[action]))
                else:
                    different.append((action, data1[action], data2[action]))

        return (only_host1, only_host2, matching, different)

    def copy(self, from_host, to_host, copy_actions):
        for host in [from_host, to_host]:
            if host not in self.hosts:
                raise RuntimeError(f'Host {host} does not exist')

        table = self.db.load_table('keybindings')

        for action in copy_actions:
            if action not in self.actions:
                raise RuntimeError(f'Action {action} does not exist')
            if self.data[from_host][action] is None:
                raise RuntimeError(f'Cannot copy missing keys for action {action}')

            if self.data[from_host][action] == self.data[to_host][action]:
                continue

            row = {
                'hostname': to_host,
                'context': action[0],
                'action': action[1],
                'keylist': self.data[from_host][action],
                'description': table.find_one(
                    hostname = from_host,
                    context = action[0],
                    action = action[1],
                )['description'],
            }

            table.upsert(row, keys = ['hostname', 'context', 'action'])
            self.data[to_host][action] = self.data[from_host][action]


class JumpPoints:
    def __init__(self, db):
        self.db = db

        self.hosts = [
            row['hostname']
            for row in db.load_table('jumppoints').distinct('hostname')
        ]

        self.dests = [
            row['destination']
            for row in db.load_table('jumppoints').distinct('destination')
        ]

        self.data = {}
        for host in self.hosts:
            self.data[host] = {}
            for dest in self.dests:
                self.data[host][dest] = None
        for row in db.load_table('jumppoints'):
            host = row['hostname']
            dest = row['destination']
            keys = row['keylist']
            self.data[host][dest] = keys

    def compare(self, host1, host2):
        for host in [host1, host2]:
            if host not in self.hosts:
                raise RuntimeError(f'Host {host} does not exist')

        only_host1 = []
        only_host2 = []
        matching = []
        different = []

        data1 = self.data[host1]
        data2 = self.data[host2]

        for dest in self.dests:
            if data1[dest] is not None and data2[dest] is None:
                only_host1.append((dest, data1[dest]))
            elif data2[dest] is not None and data1[dest] is None:
                only_host2.append((dest, data2[dest]))
            else:
                if data1[dest] == data2[dest]:
                    matching.append((dest, data1[dest]))
                else:
                    different.append((dest, data1[dest], data2[dest]))

        return (only_host1, only_host2, matching, different)

    def copy(self, from_host, to_host, copy_dests):
        for host in [from_host, to_host]:
            if host not in self.hosts:
                raise RuntimeError(f'Host {host} does not exist')

        table = self.db.load_table('jumppoints')

        for dest in copy_dests:
            if dest not in self.dests:
                raise RuntimeError(f'Destination {dest} does not exist')
            if self.data[from_host][dest] is None:
                raise RuntimeError(f'Cannot copy missing keys for destination {dest}')

            if self.data[from_host][dest] == self.data[to_host][dest]:
                continue

            row = {
                'hostname': to_host,
                'destination': dest,
                'keylist': self.data[from_host][dest],
                'description': table.find_one(
                    hostname = from_host,
                    destination = dest,
                )['description'],
            }

            table.upsert(row, keys = ['hostname', 'destination'])
            self.data[to_host][dest] = self.data[from_host][dest]
