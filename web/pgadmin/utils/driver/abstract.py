##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2015, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
from abc import ABCMeta, abstractmethod, abstractproperty
from flask import session
from .registry import DriverRegistry


class BaseDriver(object):
    """
    class BaseDriver(object):

    This is a base class for different server types.
    Inherit this class to implement different type of database driver
    implementation.

    (For PostgreSQL/Postgres Plus Advanced Server, we will be using psycopg2)

    Abstract Properties:
    -------- ----------
    * Version (string):
        Current version string for the database server

    Abstract Methods:
    -------- -------
    * get_connection(*args, **kwargs)
    - It should return a Connection class object, which may/may not be
      connected to the database server.

    * release_connection(*args, **kwargs)
    - Implement the connection release logic

    * gc()
    - Implement this function to release the connections assigned in the
      session, which has not been pinged from more than the idle timeout
      configuration.
    """
    __metaclass__ = DriverRegistry

    @abstractproperty
    def Version(cls):
        pass

    @abstractmethod
    def get_connection(self, *args, **kwargs):
        pass

    @abstractmethod
    def release_connection(self, *args, **kwargs):
        pass

    @abstractmethod
    def gc(self):
        pass


class BaseConnection(object):
    """
    class BaseConnection(object)

        It is a base class for database connection. A different connection
        drive must implement this to expose abstract methods for this server.

        General idea is to create a wrapper around the actaul driver
        implementation. It will be instantiated by the driver factory
        basically. And, they should not be instantiated directly.


    Abstract Methods:
    -------- -------
    * connect(**kwargs)
      - Define this method to connect the server using that particular driver
        implementation.

    * execute_scalar(query, params)
      - Implement this method to execute the given query and returns single
        datum result.

    * execute_2darray(query, params)
      - Implement this method to execute the given query and returns the result
        as a 2 dimentional array.

    * execute_dict(query, params)
      - Implement this method to execute the given query and returns the result
        as an array of dict (column name -> value) format.

    * connected()
      - Implement this method to get the status of the connection. It should
        return True for connected, otherwise False

    * reset()
      - Implement this method to reconnect the database server (if possible)

    * transaction_status()
      - Implement this method to get the transaction status for this
        connection. Range of return values different for each driver type.

    * ping()
      - Implement this method to ping the server. There are times, a connection
        has been lost, but - the connection driver does not know about it. This
        can be helpful to figure out the actual reason for query failure.

    * _release()
      - Implement this method to release the connection object. This should not
        be directly called using the connection object itself.

      NOTE: Please use BaseDriver.release_connection(...) for releasing the
            connection object for better memory management, and connection pool
            management.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def execute_scalar(self, query, params=None):
        pass

    @abstractmethod
    def execute_2darray(self, query, params=None):
        pass

    @abstractmethod
    def execute_dict(self, query, params=None):
        pass

    @abstractmethod
    def connected(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def transaction_status(self):
        pass

    @abstractmethod
    def ping(self):
        pass

    @abstractmethod
    def _release(self):
        pass