#script that  create  complete  Vpc
#!/usr/bin/python
import boto3
client=boto3.client('ec2')
#creates VPC(id1)
response=client.create_vpc(CidrBlock='192.68.0.0/16', InstanceTenancy='default')
var=response['Vpc']
vpc_id=var['VpcId']
#creating  Public Subnet(id3)
response=client.create_subnet(CidrBlock='192.68.3.0/24',VpcId=vpc_id)
var=response['Subnet']
publicsub_id=var['SubnetId']
response = client.create_tags(Resources=[publicsub_id], Tags=[{
           'Key': 'Name',
           'Value': 'Public'
       }
    ]
)
#creating private subnet(id2)
response=client.create_subnet(CidrBlock='192.68.2.0/24',VpcId=vpc_id)
var=response['Subnet']
privatesub_id=var['SubnetId']
response = client.create_tags(Resources=[privatesub_id], Tags=[{
           'Key': 'Name',
           'Value': 'Private'
       }]) 
#creating  Public Route Tables(id4)
response=client.create_route_table(VpcId=vpc_id)
var=response['RouteTable']
publicroute_id=var['RouteTableId']
response = client.create_tags(Resources=[publicroute_id], Tags=[{
           'Key': 'Name',
           'Value': 'PublicRoute'
       } 
    ]
)
#asscoaition  with the  subnet
response = client.associate_route_table(
    RouteTableId=publicroute_id,
    SubnetId=publicsub_id
)
#Creating  private RouteTable(id4)  
response=client.create_route_table(VpcId=vpc_id)
var=response['RouteTable']
privateroute_id=var['RouteTableId']
response = client.create_tags(Resources=[privateroute_id], Tags=[{
           'Key': 'Name',
           'Value': 'PrivateRoute'
       } 
    ]
)
response = client.associate_route_table(
    RouteTableId=privateroute_id,
    SubnetId=privatesub_id
)
#Creating  Internet gateway

response=client.create_internet_gateway()
var=response['InternetGateway']
gateway_id=var['InternetGatewayId']

#Attaching  InternetGateway
response = client.attach_internet_gateway(
    InternetGatewayId=gateway_id,
    VpcId=vpc_id
)
#Attaching gateway  with  public routetable
response = client.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=gateway_id,
    RouteTableId=publicroute_id
)
#creating  ElasticIp
response=client.allocate_address(Domain='vpc')
allocation_id=response['AllocationId']
publicip=response['PublicIp']

#ceating NatGateway
response = client.create_nat_gateway(
    AllocationId=allocation_id,
    SubnetId=publicsub_id
)
var=response['NatGateway']
natgateway_id=var['NatGatewayId']

