from tests.validation.cattlevalidationtest.core.common_fixtures import *  # NOQA
import pytest

TEST_SERVICE_OPT_IMAGE = 'ibuildthecloud/helloworld'
TEST_SERVICE_OPT_IMAGE_LATEST = TEST_SERVICE_OPT_IMAGE + ':latest'
TEST_SERVICE_OPT_IMAGE_UUID = 'docker:' + TEST_SERVICE_OPT_IMAGE_LATEST
LB_IMAGE_UUID = "docker:sangeetha/testlbsd:latest"
logger = logging.getLogger(__name__)


@pytest.mark.skipif(os.environ.get('RANCHER_SERVER_VERSION') == '0.35.0',
                    reason="This release of Rancher does not support this feature")
class TestRancherComposeService:
    tname = "TestRancherComposeService"

    @pytest.mark.create
    @pytest.mark.run(order=1)
    def test_create_rancher_compose_service(self, super_client, client, rancher_compose_container, socat_containers):
        vol_container = client.create_container(imageUuid=TEST_IMAGE_UUID,
                                                name=random_str(),
                                                labels={"c1": "vol"}
                                                )
        vol_container = client.wait_success(vol_container)

        volume_in_host = "/test/container"
        volume_in_container = "/test/vol1"
        docker_vol_value = volume_in_host + ":" + volume_in_container + ":ro"

        # dict['docker_vol_value'] = docker_vol_value

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
                         "labels":
                             {"io.rancher.scheduler.affinity:container_label":
                                  "c1=vol"}
                         }

        scale = 1

        service, env = create_env_and_svc(client, launch_config,
                                          scale, self.tname)

    @pytest.mark.validate
    @pytest.mark.run(order=2)
    def test_rancher_compose_service(self, super_client, client, rancher_compose_container, socat_containers):

        service = ""
        env = client.list_environment(name="TestRancherComposeService")

        print "\n env is:", env
        print "\n test name is:", self.tname
        print "\n client is:", client
        launch_rancher_compose(client, env, self.tname)

        rancher_envs = client.list_environment(name=self.tname)
        assert len(rancher_envs) == 1
        rancher_env = rancher_envs[0]
        print "\n rancher_env is:", rancher_env
        rancher_service = get_rancher_compose_service(
            client, rancher_env.id, service)
        rancher_services = client.list_service(name="TestRancherComposeService",
                                               environmentId=rancher_env.id,
                                               removed_null=True)
        print "\n rancher_services:", rancher_services
        assert len(rancher_services) == 1
        rancher_service = rancher_services[0]
        print service.kind
        if service.kind != 'externalService' and service.kind != 'dnsService':
            assert rancher_service.scale == service.scale
        rancher_service = client.wait_success(rancher_service, 120)

        check_container_in_service(super_client, rancher_service)

        container_list = get_service_container_list(super_client, rancher_service)
        for c in container_list:
            # print c
            docker_client = get_docker_client(c.hosts[0])
            inspect = docker_client.inspect_container(c.externalId)

            assert inspect["HostConfig"]["Binds"] == [dict['docker_vol_value']]
            # assert inspect["HostConfig"]["VolumesFrom"] == \
            #        [vol_container.externalId]
            assert inspect["HostConfig"]["PublishAllPorts"] is False
            assert inspect["HostConfig"]["Privileged"] is True
            assert inspect["Config"]["OpenStdin"] is True
            assert inspect["Config"]["Tty"] is True
            assert inspect["HostConfig"]["Dns"] == dict['dns_name']
            assert inspect["HostConfig"]["DnsSearch"] == dict['dns_search']
            assert inspect["Config"]["Hostname"] == dict['host_name']
            assert inspect["Config"]["Domainname"] == dict['domain_name']
            assert inspect["Config"]["User"] == dict['user']
            assert inspect["HostConfig"]["CapAdd"] == dict['cap_add']
            assert inspect["HostConfig"]["CapDrop"] == dict['cap_drop']
            #        assert inspect["Config"]["Cpuset"] == cpu_set
            assert inspect["HostConfig"]["RestartPolicy"]["Name"] == \
                   dict['restart_policy']["name"]
            assert inspect["HostConfig"]["RestartPolicy"]["MaximumRetryCount"] == \
                   dict['restart_policy']["maximumRetryCount"]
            # assert inspect["Config"]["Cmd"] == command
            # assert inspect["Config"]["Memory"] == memory
            # assert "TEST_FILE=/etc/testpath.conf" in inspect["Config"]["Env"]
            # assert inspect["Config"]["CpuShares"] == cpu_shares

        print("********************* VALIDATED LB BASE OBJECT ***********************")
        delete_all(client, [env])


@pytest.mark.skipif(os.environ.get('RANCHER_SERVER_VERSION') == '0.34.0',
                    reason="This release of Rancher does not support this feature")
class TestRancherComposeLBService:
    tname = "TestRancherComposeLBService"

    @pytest.mark.create
    @pytest.mark.run(order=1)
    def test_rancher_compose_lbservice_create(self, super_client, client,
                                              rancher_compose_container):
        port = "7900"

        # Add LB service and do not activate services
        service_scale = 2
        lb_scale = 1

        env, service, lb_service = create_env_with_svc_and_lb(
            client, service_scale, lb_scale, port, self.tname)

        service_link = {"serviceId": service.id, "ports": ["80"]}
        lb_service.addservicelink(serviceLink=service_link)

        validate_add_service_link(super_client, lb_service, service)

        # Add another service link to the LB service
        launch_config = {"imageUuid": WEB_IMAGE_UUID}
        service_name = self.tname + "1"
        service1 = client.create_service(name=service_name,
                                         environmentId=env.id,
                                         launchConfig=launch_config,
                                         scale=2)
        service1 = client.wait_success(service1)
        assert service1.state == "inactive"

        service_link = {"serviceId": service1.id, "ports": ["80"]}
        lb_service.addservicelink(serviceLink=service_link)
        validate_add_service_link(super_client, lb_service, service1)

        launch_rancher_compose(client, env, self.tname)
        delete_all(super_client, [env])
        client.delete()


    @pytest.mark.validate
    @pytest.mark.run(order=2)
    def test_rancher_compose_lbservice_validate(self, super_client, client,
                                                rancher_compose_container):
        port = "7900"
        env1 = client.list_environment(name="testranchercomposelbservicerancher")
        print "\n\n\n env is:", env1

        services = client.list_service(name="TestRancherComposeLBService")
        assert len(services) > 0
        service = services[0]
        print "\n\n\n service is:", service

        services1 = client.list_service(name="TestRancherComposeLBService1")
        assert len(services1) > 0
        service1 =  services1[0]
        print "\n\n\n service1 is:", service1

        lb_services = client.list_service(name="TestRancherComposeLBServiceLB")
        assert len(lb_services) > 0
        lb_service = lb_services[0]
        print "\n\n\n lb_service is:", lb_service

        rancher_envs = client.list_environment(name="testranchercomposelbservicerancher")

        print "\n\n\n rancher_envs is:", rancher_envs

        assert len(rancher_envs) > 0
        rancher_env = rancher_envs[0]

        print "\n\n\n rancher_env is:", rancher_env

        rancher_service = get_rancher_compose_service(
            client, rancher_env.id, service)
        rancher_service1 = get_rancher_compose_service(
            client, rancher_env.id, service1)
        rancher_lb_service = get_rancher_compose_service(
            client, rancher_env.id, lb_service)

        client.wait_success(rancher_service)
        client.wait_success(rancher_service1)
        client.wait_success(rancher_lb_service)
        validate_add_service_link(
            super_client, rancher_lb_service, rancher_service)
        validate_add_service_link(
            super_client, rancher_lb_service, rancher_service1)

        validate_lb_service(super_client, client, rancher_lb_service, port,
                            [rancher_service, rancher_service1])
        #delete_all(super_client, [env1])


def get_rancher_compose_service(client, rancher_env_id, service):
    rancher_services = client.list_service(name=service.name,
                                           environmentId=rancher_env_id,
                                           removed_null=True)
    print "\n\n\n rancher_services is:", rancher_services
    assert len(rancher_services) == 1
    rancher_service = rancher_services[0]
    print service.kind
    if service.kind != 'externalService' and service.kind != 'dnsService':
        assert rancher_service.scale == service.scale
    rancher_service = client.wait_success(rancher_service, 120)
    return rancher_service


def get_service_container_list(super_client, service):
    container = []
    instance_maps = super_client.list_serviceExposeMap(serviceId=service.id,
                                                       state="active")
    for instance_map in instance_maps:
        c = super_client.by_id('container', instance_map.instanceId)
        containers = super_client.list_container(
            externalId=c.externalId,
            include="hosts")
        assert len(containers) == 1
        container.append(containers[0])

    return container
