from common_fixtures import *  # NOQA
import pytest

TEST_SERVICE_OPT_IMAGE = 'ibuildthecloud/helloworld'
TEST_SERVICE_OPT_IMAGE_LATEST = TEST_SERVICE_OPT_IMAGE + ':latest'
TEST_SERVICE_OPT_IMAGE_UUID = 'docker:' + TEST_SERVICE_OPT_IMAGE_LATEST

LB_IMAGE_UUID = "docker:sangeetha/testlbsd:latest"
SSH_IMAGE_UUID = "docker:sangeetha/testclient:latest"

docker_config_running = [{"docker_param_name": "State.Running",
                          "docker_param_value": "true"}]

docker_config_stopped = [{"docker_param_name": "State.Running",
                          "docker_param_value": "false"}]

logger = logging.getLogger(__name__)

total_time = [0]
shared_env = []



# @pytest.fixture(scope='session', autouse=True)
# def create_env_for_activate_deactivate(request, client, super_client):
#     service, env = create_env_and_svc_activate(super_client, client, 3, False)
#     shared_env.append({"service": service,
#                        "env": env})
#
#     def fin():
#         to_delete = [env]
#         delete_all(client, to_delete)
#
#     request.addfinalizer(fin)
#
#
# def deactivate_activate_service(super_client, client, service):
#     # Deactivate service
#     service = service.deactivate()
#     service = client.wait_success(service, 300)
#     assert service.state == "inactive"
#     # Activate Service
#     service = service.activate()
#     service = client.wait_success(service, 300)
#     assert service.state == "active"
#     return service
#
#
# def create_env_and_svc_activate(super_client, client, scale, check=True):
#     start_time = time.time()
#     launch_config = {"imageUuid": TEST_IMAGE_UUID}
#     service, env = create_env_and_svc(client, launch_config, scale)
#     service = service.activate()
#     service = client.wait_success(service, 300)
#     assert service.state == "active"
#     if check:
#         check_container_in_service(super_client, service)
#     time_taken = time.time() - start_time
#     total_time[0] = total_time[0] + time_taken
#     logger.info("time taken - " + str(time_taken))
#     logger.info("total time taken - " + str(total_time[0]))
#     return service, env

@pytest.mark.skipif(1 != 2, reason="Original: only for reference")
def test_services_docker_options(super_client, client, socat_containers):
    testname = "TestServicesDockerOptions"
    hosts = client.list_host(kind='docker', removed_null=True, state="active")
    print "\n\n\n hosts is:", hosts
    con_host = hosts[0]
    print "\n\n\n con_host is:", con_host
    vol_container = client.create_container(imageUuid=TEST_IMAGE_UUID,
                                            name=random_str(),
                                            requestedHostId=con_host.id
                                            )
    vol_container = client.wait_success(vol_container)
    volume_in_host = "/test/container"
    volume_in_container = "/test/vol1"
    docker_vol_value = volume_in_host + ":" + volume_in_container + ":ro"
    cap_add = ["CHOWN"]
    cap_drop = ["KILL"]
    restart_policy = {"maximumRetryCount": 10, "name": "on-failure"}
    dns_search = ['1.2.3.4']
    dns_name = ['1.2.3.4']
    domain_name = "rancher.io"
    host_name = "test"
    user = "root"
    command = ["sleep", "9000"]
    env_var = {"TEST_FILE": "/etc/testpath.conf"}
    memory = 8000000
    cpu_set = "0"
    cpu_shares = 400
    launch_config = {"imageUuid": TEST_SERVICE_OPT_IMAGE_UUID,
                     "command": command,
                     "dataVolumes": [docker_vol_value],
                     "dataVolumesFrom": [vol_container.id],
                     "environment": env_var,
                     "capAdd": cap_add,
                     "capDrop": cap_drop,
                     "dnsSearch": dns_search,
                     "dns": dns_name,
                     "privileged": True,
                     "domainName": domain_name,
                     "stdinOpen": True,
                     "tty": True,
                     "memory": memory,
                     "cpuSet": cpu_set,
                     "cpuShares": cpu_shares,
                     "restartPolicy": restart_policy,
                     "directory": "/",
                     "hostname": host_name,
                     "user": user,
                     "requestedHostId": con_host.id
                     }
    scale = 2
    service, env = create_env_and_svc(client, launch_config,
                                      scale, testname)
    env = env.activateservices()
    print "\n\n\n env is:", env
    service = client.wait_success(service, 300)
    print "\n\n\n service is:", service
    assert service.state == "active"
    check_container_in_service(super_client, service)
    container_list = get_service_container_list(super_client, service)
    for c in container_list:
        print "\n\n\n container is:", c
        print "\n\n\n c.host is:", (c.hosts[0])
        docker_client = get_docker_client(c.hosts[0])
        print "\n\n\n docker_client is:", docker_client
        inspect = docker_client.inspect_container(c.externalId)
        print "\n\n\n inspect is:", inspect
        assert inspect["HostConfig"]["Binds"] == [docker_vol_value]
        assert inspect["HostConfig"]["VolumesFrom"] == \
            [vol_container.externalId]
        assert inspect["HostConfig"]["PublishAllPorts"] is False
        assert inspect["HostConfig"]["Privileged"] is True
        assert inspect["Config"]["OpenStdin"] is True
        assert inspect["Config"]["Tty"] is True
        assert inspect["HostConfig"]["Dns"] == dns_name
        assert inspect["HostConfig"]["DnsSearch"] == dns_search
        assert inspect["Config"]["Hostname"] == host_name
        assert inspect["Config"]["Domainname"] == domain_name
        assert inspect["Config"]["User"] == user
        assert inspect["HostConfig"]["CapAdd"] == cap_add
        assert inspect["HostConfig"]["CapDrop"] == cap_drop
        assert inspect["Config"]["Cpuset"] == cpu_set
        assert inspect["HostConfig"]["RestartPolicy"]["Name"] == \
            restart_policy["name"]
        assert inspect["HostConfig"]["RestartPolicy"]["MaximumRetryCount"] == \
            restart_policy["maximumRetryCount"]
        assert inspect["Config"]["Cmd"] == command
        assert inspect["Config"]["Memory"] == memory
        assert "TEST_FILE=/etc/testpath.conf" in inspect["Config"]["Env"]
        assert inspect["Config"]["CpuShares"] == cpu_shares


@pytest.mark.skipif(os.environ.get('RANCHER_SERVER_VERSION') == '0.34.0',
                    reason="This release of Rancher does not support this feature")
class TestServicesDockerOptions:
    testname = "TestServicesDockerOptions"
    cap_add = ["CHOWN"]
    cap_drop = ["KILL"]
    restart_policy = {"maximumRetryCount": 10, "name": "on-failure"}
    dns_search = ['1.2.3.4']
    dns_name = ['1.2.3.4']
    domain_name = "rancher.io"
    host_name = "test"
    user = "root"
    command = ["sleep", "9000"]
    env_var = {"TEST_FILE": "/etc/testpath.conf"}
    memory = 8000000
    cpu_set = "0"
    cpu_shares = 400
    scale = 2
    volume_in_host = "/test/container"
    volume_in_container = "/test/vol1"
    launch_config = {"imageUuid": TEST_SERVICE_OPT_IMAGE_UUID,
                     "command": command,
                     "environment": env_var,
                     "capAdd": cap_add,
                     "capDrop": cap_drop,
                     "dnsSearch": dns_search,
                     "dns": dns_name,
                     "privileged": True,
                     "domainName": domain_name,
                     "stdinOpen": True,
                     "tty": True,
                     "memory": memory,
                     "cpuSet": cpu_set,
                     "cpuShares": cpu_shares,
                     "restartPolicy": restart_policy,
                     "directory": "/",
                     "hostname": host_name,
                     "user": user,
                     }

    @pytest.mark.create
    @pytest.mark.run(order=1)
    def test_services_docker_options_create(self, client, socat_containers):
        hosts = client.list_host(kind='docker', removed_null=True, state="active")
        logger.info("hosts is: %s", format(hosts))
        con_host = hosts[0]
        logger.info("con_host is: %s", format(con_host))
        vol_container = client.create_container(imageUuid=TEST_IMAGE_UUID,
                                                name=random_str(),
                                                requestedHostId=con_host.id
                                                )
        vol_container = client.wait_success(vol_container)
        docker_vol_value = self.volume_in_host + ":" + self.volume_in_container + ":ro"
        launch_config = self.launch_config
        logger.info("launch_config is: %s", format(launch_config))
        launch_config.update({"dataVolumes": [docker_vol_value],
                              "dataVolumesFrom": [vol_container.id],
                              "requestedHostId": con_host.id})
        logger.info("launch_config after update is: %s", format(launch_config))
        service, env = create_env_and_svc(client, self.launch_config, self.scale, self.testname)
        env = env.activateservices()
        logger.info("env is: %s", format(env))
        service = client.wait_success(service, 300)
        logger.info("service is: %s", format(service))
        assert service.state == "active"
        data = [env.uuid, service.uuid, vol_container.uuid, launch_config]
        logger.info("data to save: %s", data)
        save(data, self)


    @pytest.mark.validate
    @pytest.mark.run(order=2)
    def test_services_docker_options_validate(self, super_client, client, socat_containers):
        data = load(self)
        env = client.list_environment(uuid=data[0])
        logger.info("env is: %s", format(env))
        services = client.list_service(uuid=data[1])
        assert len(services) > 0
        service = services[0]
        logger.info("service is: %s", format(service))
        #service = client.wait_success(service, 300)
        assert service.state == "active"
        check_container_in_service(super_client, service)
        vol_container = client.list_container(uuid=data[2])
        logger.info("vol_container is: %s", format(vol_container))
        launch_config = service.launchConfig
        logger.info("launch_config is: %s", format(launch_config))
        container_list = get_service_container_list(super_client, service)
        for c in container_list:
            logger.info("container is: %s", format(c))
            logger.info("container's host is: %s", c.hosts[0])
            docker_client = get_docker_client(c.hosts[0])
            logger.info("docker client is: %s", docker_client)
            logger.info("container's externalId is: %s", c.externalId)
            inspect = docker_client.inspect_container(c.externalId)
            logger.info("inspect is: %s", inspect)
            assert inspect["HostConfig"]["Binds"] == launch_config["dataVolumes"]
            #assert inspect["HostConfig"]["VolumesFrom"] == vol_container['data']['externalId']
            assert inspect["HostConfig"]["PublishAllPorts"] is False
            assert inspect["HostConfig"]["Privileged"] is True
            assert inspect["Config"]["OpenStdin"] is True
            assert inspect["Config"]["Tty"] is True
            assert inspect["HostConfig"]["Dns"] == launch_config['dns']
            assert inspect["HostConfig"]["DnsSearch"] == launch_config['dnsSearch']
            assert inspect["Config"]["Hostname"] == launch_config['hostname']
            assert inspect["Config"]["Domainname"] == launch_config['domainName']
            assert inspect["Config"]["User"] == launch_config['user']
            assert inspect["HostConfig"]["CapAdd"] == launch_config['capAdd']
            assert inspect["HostConfig"]["CapDrop"] == launch_config['capDrop']
            assert inspect["Config"]["Cpuset"] == launch_config['cpuSet']
            assert inspect["HostConfig"]["RestartPolicy"]["Name"] == \
                   launch_config['restartPolicy']['name']
            assert inspect["HostConfig"]["RestartPolicy"]["MaximumRetryCount"] == \
                   launch_config['restartPolicy']['maximumRetryCount']
            assert inspect["Config"]["Cmd"] == launch_config['command']
            assert inspect["Config"]["Memory"] == launch_config['memory']
            assert "TEST_FILE=/etc/testpath.conf" in inspect["Config"]["Env"]
            assert inspect["Config"]["CpuShares"] == launch_config['cpuShares']

