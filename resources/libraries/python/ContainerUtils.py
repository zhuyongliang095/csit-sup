# Copyright (c) 2017 Cisco and/or its affiliates.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Bug workaround in pylint for abstract classes.
# pylint: disable=W0223

"""Library to manipulate Containers."""

from collections import OrderedDict, Counter

from resources.libraries.python.ssh import SSH
from resources.libraries.python.constants import Constants
from resources.libraries.python.CpuUtils import CpuUtils
from resources.libraries.python.VppConfigGenerator import VppConfigGenerator


__all__ = ["ContainerManager", "ContainerEngine", "LXC", "Docker", "Container"]

SUPERVISOR_CONF = '/etc/supervisord.conf'


class ContainerManager(object):
    """Container lifecycle management class."""

    def __init__(self, engine):
        """Initialize Container Manager class.

        :param engine: Container technology used (LXC/Docker/...).
        :type engine: str
        :raises NotImplementedError: If container technology is not implemented.
        """
        try:
            self.engine = globals()[engine]()
        except KeyError:
            raise NotImplementedError('{e} is not implemented.'
                                      .format(e=engine))
        self.containers = OrderedDict()

    def get_container_by_name(self, name):
        """Get container instance.

        :param name: Container name.
        :type name: str
        :returns: Container instance.
        :rtype: Container
        :raises RuntimeError: If failed to get container with name.
        """
        try:
            return self.containers[name]
        except KeyError:
            raise RuntimeError('Failed to get container with name: {n}'
                               .format(n=name))

    def construct_container(self, **kwargs):
        """Construct container object on node with specified parameters.

        :param kwargs: Key-value pairs used to construct container.
        :param kwargs: dict
        """
        # Create base class
        self.engine.initialize()
        # Set parameters
        for key in kwargs:
            setattr(self.engine.container, key, kwargs[key])

        # Set additional environmental variables
        setattr(self.engine.container, 'env',
                'MICROSERVICE_LABEL={n}'.format(n=kwargs['name']))

        # Set cpuset.cpus cgroup
        skip_cnt = kwargs['cpu_skip']
        if not kwargs['cpu_shared']:
            skip_cnt += kwargs['i'] * kwargs['cpu_count']
        self.engine.container.cpuset_cpus = \
            CpuUtils.cpu_slice_of_list_per_node(node=kwargs['node'],
                                                cpu_node=kwargs['cpuset_mems'],
                                                skip_cnt=skip_cnt,
                                                cpu_cnt=kwargs['cpu_count'],
                                                smt_used=kwargs['smt_used'])

        # Store container instance
        self.containers[kwargs['name']] = self.engine.container

    def construct_containers(self, **kwargs):
        """Construct 1..N container(s) on node with specified name.

        Ordinal number is automatically added to the name of container as
        suffix.

        :param kwargs: Named parameters.
        :param kwargs: dict
        """
        name = kwargs['name']
        for i in range(kwargs['count']):
            # Name will contain ordinal suffix
            kwargs['name'] = ''.join([name, str(i+1)])
            # Create container
            self.construct_container(i=i, **kwargs)

    def acquire_all_containers(self):
        """Acquire all containers."""
        for container in self.containers:
            self.engine.container = self.containers[container]
            self.engine.acquire()

    def build_all_containers(self):
        """Build all containers."""
        for container in self.containers:
            self.engine.container = self.containers[container]
            self.engine.build()

    def create_all_containers(self):
        """Create all containers."""
        for container in self.containers:
            self.engine.container = self.containers[container]
            self.engine.create()

    def execute_on_container(self, name, command):
        """Execute command on container with name.

        :param name: Container name.
        :param command: Command to execute.
        :type name: str
        :type command: str
        """
        self.engine.container = self.get_container_by_name(name)
        self.engine.execute(command)

    def execute_on_all_containers(self, command):
        """Execute command on all containers.

        :param command: Command to execute.
        :type command: str
        """
        for container in self.containers:
            self.engine.container = self.containers[container]
            self.engine.execute(command)

    def install_vpp_in_all_containers(self):
        """Install VPP into all containers."""
        for container in self.containers:
            self.engine.container = self.containers[container]
            # We need to install supervisor client/server system to control VPP
            # as a service
            self.engine.install_supervisor()
            self.engine.install_vpp()
            self.engine.restart_vpp()

    def configure_vpp_in_all_containers(self, vat_template_file):
        """Configure VPP in all containers.

        :param vat_template_file: Template file name of a VAT script.
        :type vat_template_file: str
        """
        # Count number of DUTs based on node's host information
        dut_cnt = len(Counter([self.containers[container].node['host']
                               for container in self.containers]))
        container_cnt = len(self.containers)
        mod = dut_cnt/container_cnt

        for i, container in enumerate(self.containers):
            self.engine.container = self.containers[container]
            self.engine.create_vpp_startup_config()
            self.engine.create_vpp_exec_config(vat_template_file,
                                               memif_id1=i % mod * 2 + 1,
                                               memif_id2=i % mod * 2 + 2,
                                               socket1='memif-{c.name}-1'
                                               .format(c=self.engine.container),
                                               socket2='memif-{c.name}-2'
                                               .format(c=self.engine.container))

    def stop_all_containers(self):
        """Stop all containers."""
        for container in self.containers:
            self.engine.container = self.containers[container]
            self.engine.stop()

    def destroy_all_containers(self):
        """Destroy all containers."""
        for container in self.containers:
            self.engine.container = self.containers[container]
            self.engine.destroy()


class ContainerEngine(object):
    """Abstract class for container engine."""

    def __init__(self):
        """Init ContainerEngine object."""
        self.container = None

    def initialize(self):
        """Initialize container object."""
        self.container = Container()

    def acquire(self, force):
        """Acquire/download container.

        :param force: Destroy a container if exists and create.
        :type force: bool
        """
        raise NotImplementedError

    def build(self):
        """Build container (compile)."""
        raise NotImplementedError

    def create(self):
        """Create/deploy container."""
        raise NotImplementedError

    def execute(self, command):
        """Execute process inside container.

        :param command: Command to run inside container.
        :type command: str
        """
        raise NotImplementedError

    def stop(self):
        """Stop container."""
        raise NotImplementedError

    def destroy(self):
        """Destroy/remove container."""
        raise NotImplementedError

    def info(self):
        """Info about container."""
        raise NotImplementedError

    def system_info(self):
        """System info."""
        raise NotImplementedError

    def install_supervisor(self):
        """Install supervisord inside a container."""
        self.execute('sleep 3')
        self.execute('apt-get update')
        self.execute('apt-get install -y supervisor')
        self.execute('echo "{0}" > {1}'
                     .format(
                         '[unix_http_server]\n'
                         'file  = /tmp/supervisor.sock\n\n'
                         '[rpcinterface:supervisor]\n'
                         'supervisor.rpcinterface_factory = '
                         'supervisor.rpcinterface:make_main_rpcinterface\n\n'
                         '[supervisorctl]\n'
                         'serverurl = unix:///tmp/supervisor.sock\n\n'
                         '[supervisord]\n'
                         'pidfile = /tmp/supervisord.pid\n'
                         'identifier = supervisor\n'
                         'directory = /tmp\n'
                         'logfile=/tmp/supervisord.log\n'
                         'loglevel=debug\n'
                         'nodaemon=false\n\n',
                         SUPERVISOR_CONF))
        self.execute('supervisord -c {0}'.format(SUPERVISOR_CONF))

    def install_vpp(self, install_dkms=False):
        """Install VPP inside a container.

        :param install_dkms: If install dkms package. This will impact install
        time. Dkms is required for installation of vpp-dpdk-dkms. Default is
        false.
        :type install_dkms: bool
        """
        self.execute('ln -s /dev/null /etc/sysctl.d/80-vpp.conf')
        self.execute('apt-get update')
        if install_dkms:
            self.execute('apt-get install -y dkms && '
                         'dpkg -i --force-all {0}/install_dir/*.deb'
                         .format(self.container.guest_dir))
        else:
            self.execute('for i in $(ls -I \"*dkms*\" {0}/install_dir/); '
                         'do dpkg -i --force-all {0}/install_dir/$i; done'
                         .format(self.container.guest_dir))
        self.execute('apt-get -f install -y')
        self.execute('echo "{0}" >> {1}'
                     .format(
                         '[program:vpp]\n'
                         'command=/usr/bin/vpp -c /etc/vpp/startup.conf\n'
                         'autorestart=false\n'
                         'redirect_stderr=true\n'
                         'priority=1',
                         SUPERVISOR_CONF))
        self.execute('supervisorctl reload')

    def restart_vpp(self):
        """Restart VPP service inside a container."""
        self.execute('supervisorctl restart vpp')

    def create_vpp_startup_config(self,
                                  config_filename='/etc/vpp/startup.conf'):
        """Create base startup configuration of VPP on container.

        :param config_filename: Startup configuration file name.
        :type config_filename: str
        """
        cpuset_cpus = self.container.cpuset_cpus

        # Create config instance
        vpp_config = VppConfigGenerator()
        vpp_config.set_node(self.container.node)
        vpp_config.add_unix_cli_listen()
        vpp_config.add_unix_nodaemon()
        vpp_config.add_unix_exec('/tmp/running.exec')
        # We will pop first core from list to be main core
        vpp_config.add_cpu_main_core(str(cpuset_cpus.pop(0)))
        # if this is not only core in list, the rest will be used as workers.
        if cpuset_cpus:
            corelist_workers = ','.join(str(cpu) for cpu in cpuset_cpus)
            vpp_config.add_cpu_corelist_workers(corelist_workers)
        vpp_config.add_plugin_disable('dpdk_plugin.so')

        self.execute('mkdir -p /etc/vpp/')
        self.execute('echo "{c}" | tee {f}'
                     .format(c=vpp_config.get_config_str(),
                             f=config_filename))

    def create_vpp_exec_config(self, vat_template_file, **kwargs):
        """Create VPP exec configuration on container.

        :param vat_template_file: File name of a VAT template script.
        :param kwargs: Parameters for VAT script.
        :type vat_template_file: str
        :type kwargs: dict
        """
        vat_file_path = '{p}/{f}'.format(p=Constants.RESOURCES_TPL_VAT,
                                         f=vat_template_file)

        with open(vat_file_path, 'r') as template_file:
            cmd_template = template_file.readlines()
            for line_tmpl in cmd_template:
                vat_cmd = line_tmpl.format(**kwargs)
                self.execute('echo "{c}" >> /tmp/running.exec'
                             .format(c=vat_cmd.replace('\n', '')))

    def is_container_running(self):
        """Check if container is running."""
        raise NotImplementedError

    def is_container_present(self):
        """Check if container is present."""
        raise NotImplementedError

    def _configure_cgroup(self, name):
        """Configure the control group associated with a container.

        :param name: Name of cgroup.
        :type name: str
        :raises RuntimeError: If applying cgroup settings via cgset failed.
        """
        ret, _, _ = self.container.ssh.exec_command_sudo(
            'cgcreate -g cpuset:/{name}'.format(name=name))
        if int(ret) != 0:
            raise RuntimeError('Failed to copy cgroup settings from root.')

        ret, _, _ = self.container.ssh.exec_command_sudo(
            'cgset -r cpuset.cpu_exclusive=0 /{name}'.format(name=name))
        if int(ret) != 0:
            raise RuntimeError('Failed to apply cgroup settings.')

        ret, _, _ = self.container.ssh.exec_command_sudo(
            'cgset -r cpuset.mem_exclusive=0 /{name}'.format(name=name))
        if int(ret) != 0:
            raise RuntimeError('Failed to apply cgroup settings.')


class LXC(ContainerEngine):
    """LXC implementation."""

    def __init__(self):
        """Initialize LXC object."""
        super(LXC, self).__init__()

    def acquire(self, force=True):
        """Acquire a privileged system object where configuration is stored.

        :param force: If a container exists, destroy it and create a new
        container.
        :type force: bool
        :raises RuntimeError: If creating the container or writing the container
        config fails.
        """
        if self.is_container_present():
            if force:
                self.destroy()
            else:
                return

        image = self.container.image if self.container.image else\
            "-d ubuntu -r xenial -a amd64"

        cmd = 'lxc-create -t download --name {c.name} -- {image} '\
            '--no-validate'.format(c=self.container, image=image)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd, timeout=1800)
        if int(ret) != 0:
            raise RuntimeError('Failed to create container.')

        if self.container.host_dir and self.container.guest_dir:
            entry = 'lxc.mount.entry = '\
                '{c.host_dir} /var/lib/lxc/{c.name}/rootfs{c.guest_dir} ' \
                'none bind,create=dir 0 0'.format(c=self.container)
            ret, _, _ = self.container.ssh.exec_command_sudo(
                "sh -c 'echo \"{e}\" >> /var/lib/lxc/{c.name}/config'"
                .format(e=entry, c=self.container))
            if int(ret) != 0:
                raise RuntimeError('Failed to write {c.name} config.'
                                   .format(c=self.container))
        self._configure_cgroup('lxc')

    def create(self):
        """Create/deploy an application inside a container on system.

        :raises RuntimeError: If creating the container fails.
        """
        cpuset_cpus = '{0}'.format(
            ','.join('%s' % cpu for cpu in self.container.cpuset_cpus))\
            if self.container.cpuset_cpus else ''

        cmd = 'lxc-start --name {c.name} --daemon'.format(c=self.container)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to start container {c.name}.'
                               .format(c=self.container))
        self._lxc_wait('RUNNING')

        # Workaround for LXC to be able to allocate all cpus including isolated.
        cmd = 'cgset --copy-from / lxc/'
        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to copy cgroup to LXC')

        cmd = 'lxc-cgroup --name {c.name} cpuset.cpus {cpus}'\
            .format(c=self.container, cpus=cpuset_cpus)
        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to set cpuset.cpus to container '
                               '{c.name}.'.format(c=self.container))

    def execute(self, command):
        """Start a process inside a running container.

        Runs the specified command inside the container specified by name. The
        container has to be running already.

        :param command: Command to run inside container.
        :type command: str
        :raises RuntimeError: If running the command failed.
        """
        env = '--keep-env {0}'.format(
            ' '.join('--set-var %s' % env for env in self.container.env))\
            if self.container.env else ''

        cmd = "lxc-attach {env} --name {c.name} -- /bin/sh -c '{command}'"\
            .format(env=env, c=self.container, command=command)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd, timeout=180)
        if int(ret) != 0:
            raise RuntimeError('Failed to run command inside container '
                               '{c.name}.'.format(c=self.container))

    def stop(self):
        """Stop a container.

        :raises RuntimeError: If stopping the container failed.
        """
        cmd = 'lxc-stop --name {c.name}'.format(c=self.container)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to stop container {c.name}.'
                               .format(c=self.container))
        self._lxc_wait('STOPPED|FROZEN')

    def destroy(self):
        """Destroy a container.

        :raises RuntimeError: If destroying container failed.
        """
        cmd = 'lxc-destroy --force --name {c.name}'.format(c=self.container)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to destroy container {c.name}.'
                               .format(c=self.container))

    def info(self):
        """Query and shows information about a container.

        :raises RuntimeError: If getting info about a container failed.
        """
        cmd = 'lxc-info --name {c.name}'.format(c=self.container)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to get info about container {c.name}.'
                               .format(c=self.container))

    def system_info(self):
        """Check the current kernel for LXC support.

        :raises RuntimeError: If checking LXC support failed.
        """
        cmd = 'lxc-checkconfig'

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to check LXC support.')

    def is_container_running(self):
        """Check if container is running on node.

        :returns: True if container is running.
        :rtype: bool
        :raises RuntimeError: If getting info about a container failed.
        """
        cmd = 'lxc-info --no-humanize --state --name {c.name}'\
            .format(c=self.container)

        ret, stdout, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to get info about container {c.name}.'
                               .format(c=self.container))
        return True if 'RUNNING' in stdout else False

    def is_container_present(self):
        """Check if container is existing on node.

        :returns: True if container is present.
        :rtype: bool
        :raises RuntimeError: If getting info about a container failed.
        """
        cmd = 'lxc-info --no-humanize --name {c.name}'.format(c=self.container)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        return False if int(ret) else True

    def _lxc_wait(self, state):
        """Wait for a specific container state.

        :param state: Specify the container state(s) to wait for.
        :type state: str
        :raises RuntimeError: If waiting for state of a container failed.
        """
        cmd = 'lxc-wait --name {c.name} --state "{s}"'\
            .format(c=self.container, s=state)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to wait for state "{s}" of container '
                               '{c.name}.'.format(s=state, c=self.container))


class Docker(ContainerEngine):
    """Docker implementation."""

    def __init__(self):
        """Initialize Docker object."""
        super(Docker, self).__init__()

    def acquire(self, force=True):
        """Pull an image or a repository from a registry.

        :param force: Destroy a container if exists.
        :type force: bool
        :raises RuntimeError: If pulling a container failed.
        """
        if self.is_container_present():
            if force:
                self.destroy()
            else:
                return

        cmd = 'docker pull {c.image}'.format(c=self.container)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd, timeout=1800)
        if int(ret) != 0:
            raise RuntimeError('Failed to create container {c.name}.'
                               .format(c=self.container))
        self._configure_cgroup('docker')

    def create(self):
        """Create/deploy container.

        :raises RuntimeError: If creating a container failed.
        """
        cpuset_cpus = '--cpuset-cpus={0}'.format(
            ','.join('%s' % cpu for cpu in self.container.cpuset_cpus))\
            if self.container.cpuset_cpus else ''

        cpuset_mems = '--cpuset-mems={0}'.format(self.container.cpuset_mems)\
            if self.container.cpuset_mems is not None else ''

        env = '{0}'.format(
            ' '.join('--env %s' % env for env in self.container.env))\
            if self.container.env else ''

        command = '{0}'.format(self.container.command)\
            if self.container.command else ''

        publish = '{0}'.format(
            ' '.join('--publish %s' % var for var in self.container.publish))\
            if self.container.publish else ''

        volume = '--volume {c.host_dir}:{c.guest_dir}'.format(c=self.container)\
            if self.container.host_dir and self.container.guest_dir else ''

        cmd = 'docker run '\
            '--privileged --detach --interactive --tty --rm '\
            '--cgroup-parent docker {cpuset_cpus} {cpuset_mems} {publish} '\
            '{env} {volume} --name {container.name} {container.image} '\
            '{command}'.format(cpuset_cpus=cpuset_cpus, cpuset_mems=cpuset_mems,
                               container=self.container, command=command,
                               env=env, publish=publish, volume=volume)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to create container {c.name}'
                               .format(c=self.container))

        self.info()

    def execute(self, command):
        """Start a process inside a running container.

        Runs the specified command inside the container specified by name. The
        container has to be running already.

        :param command: Command to run inside container.
        :type command: str
        :raises RuntimeError: If runnig the command in a container failed.
        """
        cmd = "docker exec --interactive {c.name} /bin/sh -c '{command}'"\
            .format(c=self.container, command=command)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd, timeout=180)
        if int(ret) != 0:
            raise RuntimeError('Failed to execute command in container '
                               '{c.name}.'.format(c=self.container))

    def stop(self):
        """Stop running container.

        :raises RuntimeError: If stopping a container failed.
        """
        cmd = 'docker stop {c.name}'.format(c=self.container)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to stop container {c.name}.'
                               .format(c=self.container))

    def destroy(self):
        """Remove a container.

        :raises RuntimeError: If removing a container failed.
        """
        cmd = 'docker rm --force {c.name}'.format(c=self.container)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to destroy container {c.name}.'
                               .format(c=self.container))

    def info(self):
        """Return low-level information on Docker objects.

        :raises RuntimeError: If getting info about a container failed.
        """
        cmd = 'docker inspect {c.name}'.format(c=self.container)

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to get info about container {c.name}.'
                               .format(c=self.container))

    def system_info(self):
        """Display the docker system-wide information.

        :raises RuntimeError: If displaying system information failed.
        """
        cmd = 'docker system info'

        ret, _, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to get system info.')

    def is_container_present(self):
        """Check if container is present on node.

        :returns: True if container is present.
        :rtype: bool
        :raises RuntimeError: If getting info about a container failed.
        """
        cmd = 'docker ps --all --quiet --filter name={c.name}'\
            .format(c=self.container)

        ret, stdout, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to get info about container {c.name}.'
                               .format(c=self.container))
        return True if stdout else False

    def is_container_running(self):
        """Check if container is running on node.

        :returns: True if container is running.
        :rtype: bool
        :raises RuntimeError: If getting info about a container failed.
        """
        cmd = 'docker ps --quiet --filter name={c.name}'\
            .format(c=self.container)

        ret, stdout, _ = self.container.ssh.exec_command_sudo(cmd)
        if int(ret) != 0:
            raise RuntimeError('Failed to get info about container {c.name}.'
                               .format(c=self.container))
        return True if stdout else False


class Container(object):
    """Container class."""

    def __init__(self):
        """Initialize Container object."""
        pass

    def __getattr__(self, attr):
        """Get attribute custom implementation.

        :param attr: Attribute to get.
        :type attr: str
        :returns: Attribute value or None.
        :rtype: any
        """
        try:
            return self.__dict__[attr]
        except KeyError:
            return None

    def __setattr__(self, attr, value):
        """Set attribute custom implementation.

        :param attr: Attribute to set.
        :param value: Value to set.
        :type attr: str
        :type value: any
        """
        try:
            # Check if attribute exists
            self.__dict__[attr]
        except KeyError:
            # Creating new attribute
            if attr == 'node':
                self.__dict__['ssh'] = SSH()
                self.__dict__['ssh'].connect(value)
            self.__dict__[attr] = value
        else:
            # Updating attribute base of type
            if isinstance(self.__dict__[attr], list):
                self.__dict__[attr].append(value)
            else:
                self.__dict__[attr] = value
