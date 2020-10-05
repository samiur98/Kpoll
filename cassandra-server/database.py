from cassandra_cluster import Cluster

cluster = Cluster()
session = cluster.connect("kpoll_keyspace")

