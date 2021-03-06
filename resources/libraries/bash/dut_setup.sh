#!/bin/bash
# Copyright (c) 2016 Cisco and/or its affiliates.
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

function cmd {
    echo "[Command_start_exec] '$1'"
    echo -n "[Command_outputs] "
    eval ${@}
    echo "[Command_done_exec] '$1'"
    echo
}

echo
echo "[Command_desc] Starting ${0}"

#if [ -f "/etc/redhat-release" ]; then
#    cmd 'rpm -qai vpp*'
#else
#    cmd 'dpkg -l vpp\*'
#fi

cmd 'ps aux | grep vpp'

#cmd 'cat /etc/vpp/startup.conf'

#cmd 'sudo -S service vpp restart'

cmd 'cd ~/trunk/bin;./restartall.sh'


echo "[Command_desc] SLEEP for three seconds, so that VPP is up for sure"
cmd 'sleep 5'

cmd 'cd ~/trunk/bin;./check.sh'

cmd 'cat /proc/meminfo'

cmd 'free -m'

cmd 'ps aux | grep vpp'

cmd 'sudo dmidecode | grep UUID'

cmd 'lspci -Dnn'

if [ -f "/etc/redhat-release" ]; then
    cmd 'tail -n 100 /var/log/messages'
else
    cmd 'tail -n 100 /var/log/syslog'
fi

echo "[Command_desc] Adding dpdk-input trace"
cmd 'sudo ~/trunk/bin/vpp_api_test <<< "exec trace add dpdk-input 100"'

echo "[Command_desc] Adding vhost-user-input trace"
cmd 'sudo ~/trunk/bin/vpp_api_test <<< "exec trace add vhost-user-input 100"'
