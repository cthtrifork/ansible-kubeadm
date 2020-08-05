import ansible_runner
import os
import pytest
import tftest


@pytest.fixture
def spawn():
  tf = tftest.TerraformTest(os.path.join(os.path.dirname(__file__), 'terraform'))
  tf.setup(cleanup_on_exit=False)
  tf.apply()
  yield tf.output()
  tf.destroy()


@pytest.fixture
def inventory(spawn):
    return '{}/terraform/{}'.format(os.path.dirname(__file__), spawn['inventory'])


@pytest.fixture
def running_vm(inventory):
    result = ansible_runner.run(
        inventory=inventory,
        host_pattern='all',
        module='wait_for_connection'
    )
    fix_dns = ansible_runner.run(
        envvars={'ANSIBLE_HOST_KEY_CHECKING': 'false'},
        inventory=inventory,
        playbook=os.path.join(os.path.dirname(__file__), 'playbooks/fix-dns.yml')
    )
    assert fix_dns.status == 'successful'


@pytest.fixture
def prepared_vm(inventory, running_vm):
    docker = ansible_runner.run(
        envvars={'ANSIBLE_HOST_KEY_CHECKING': 'false'},
        inventory=inventory,
        playbook=os.path.join(os.path.dirname(__file__), 'playbooks/docker.yml')
    )
    assert docker.status == 'successful'


def test_install(inventory, prepared_vm):
    for playbook in ['00-apiserver-proxy.yml',
                     '01-site.yml']:
        result = ansible_runner.run(
            envvars={'ANSIBLE_HOST_KEY_CHECKING': 'false',
                 'ANSIBLE_FORCE_COLOR': 'true'},
            inventory=inventory,
            playbook=os.path.join(os.path.dirname(__file__), '../playbooks/', playbook)
        )
        assert result.status == 'successful'
