/* 
Author : Raphaël Lasalle
Date : 06-03-2023
 */

package DataProcessing;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.io.IOException;
import java.util.concurrent.TimeoutException;

import com.ibm.research.drl.dpt.providers.ProviderType;
import com.ibm.research.drl.dpt.providers.identifiers.IdentifierFactory;
import com.ibm.research.drl.dpt.providers.identifiers.Identifier;

import com.ibm.research.drl.dpt.vulnerability.ducc.*;
import com.ibm.research.drl.dpt.vulnerability.ducc.DUCC.Strategy;

import com.rabbitmq.client.*;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.JsonParser;

import DataProcessing.TypeIdentifier;
import DataProcessing.VulnerabilitiesIdentifier;

public class Server implements Runnable {

  // keys for parsing rabbitmq json config file
  private final String CONFIG_FILE_PATH = "config/java_rmq_config.json";
  private final String USER_KEY = "user";
  private final String PSWD_KEY = "pswd";
  private final String HOST_KEY = "host";
  private final String PORT_KEY = "port";
  private final String EXCH_NAME_KEY = "exchange_name";
  private final String EXCH_TYPE_KEY = "exchange_type";

  private final String Q_KEY  = "queues";
  private final String TIQ = "java_type_id_queue"; 
  private final String VIQ = "java_vuln_id_queue";
  private final ArrayList<String> QUEUES = new ArrayList<>(Arrays.asList(this.TIQ,this.VIQ));
  private final String JAVA_TIQ_RTK = "java_type_id";
  private final String JAVA_VIQ_RTK = "java_vuln_id";
  private final String PYTHON_TIQ_RTK = "python_type_id";
  private final String PYTHON_VIQ_RTK = "python_vuln_id";
  
  private final String Q_NAME_KEY = "queue_name";
  private final String RTK_KEY = "routing_key";
  private final String DRBL_KEY = "durable";
  private final String EXCL_KEY = "exclusive";
  private final String AUT_DEL_KEY = "auto_delete";
  
  private final String Q_ARGS_KEY = "queue_args"; 
  private final String ENCODING = "UTF-8";

  private String rabbitmq_username;
  private String rabbitmq_password;
  private String rabbitmq_host;
  private String rabbitmq_exchange_name;
  private String rabbitmq_exchange_type;
  private int rabbitmq_port;
  private Connection connection;
  private ConnectionFactory factory;
  private Channel channel;

  public Server() {

    try {

      ObjectMapper mapper = new ObjectMapper();
      Map<String, Object> config = mapper.readValue(new File(this.CONFIG_FILE_PATH), new TypeReference<Map<String,Object>>(){});
      List<Map<String, Object>> queues = (List<Map<String, Object>>) config.get(this.Q_KEY);
      
      this.rabbitmq_username = (String) config.get(this.USER_KEY);
      this.rabbitmq_password = (String) config.get(this.PSWD_KEY);
      this.rabbitmq_host = (String) config.get(this.HOST_KEY);
      this.rabbitmq_port = (int) config.get(this.PORT_KEY);
      this.rabbitmq_exchange_name = (String) config.get(this.EXCH_NAME_KEY);
      this.rabbitmq_exchange_type = (String) config.get(this.EXCH_TYPE_KEY);
    
      this.factory = new ConnectionFactory();
      this.factory.setHost(this.rabbitmq_host);
      this.factory.setPort(this.rabbitmq_port);
      this.factory.setUsername(this.rabbitmq_username);
      this.factory.setPassword(this.rabbitmq_password);

      try {

        this.connection = factory.newConnection();
        this.channel = connection.createChannel();
        this.channel.exchangeDeclare(this.rabbitmq_exchange_name,this.rabbitmq_exchange_type);

        for (Map<String, Object> queue : queues) {

          this.channel.queueDeclare(
            (String) queue.get(this.Q_NAME_KEY),
            Boolean.parseBoolean((String)queue.get(this.DRBL_KEY)),
            Boolean.parseBoolean((String)queue.get(this.EXCL_KEY)),
            Boolean.parseBoolean((String)queue.get(this.AUT_DEL_KEY)),
            (Map<String, Object>) queue.get(this.Q_ARGS_KEY)
          );

          this.channel.queueBind(
            (String) queue.get(this.Q_NAME_KEY),
            (String) config.get(this.EXCH_NAME_KEY),
            (String) queue.get(this.RTK_KEY)
          );

        }
        
      } catch (IOException | TimeoutException e) {
        e.printStackTrace();
      }

    } catch (Exception e){
      e.printStackTrace();
    }
  }

  public void run() { 
    try {
      Consumer consumer = new DefaultConsumer(channel) {

        private Server server;
        public Consumer withServer(Server server) {
          this.server = server;
          return this;
        }
        @Override
        public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
          System.out.println("handling delivery");
          String json_data = new String(body, server.ENCODING);
          ObjectMapper json_mapper = new ObjectMapper();
          json_mapper.configure(JsonParser.Feature.ALLOW_NON_NUMERIC_NUMBERS, true);

          String routing_key = envelope.getRoutingKey();
          
          try {

            if(routing_key.equals(server.JAVA_TIQ_RTK)) {
              ArrayList<ArrayList<String>> data = json_mapper.readValue(json_data,new TypeReference<ArrayList<ArrayList<String>>>() {});
              ArrayList<String> types = identify_type(data);
              String json_data_types = json_mapper.writeValueAsString(types);
              channel.basicPublish(server.rabbitmq_exchange_name, server.PYTHON_TIQ_RTK, null, json_data_types.getBytes());
            }

            else if(routing_key.equals(server.JAVA_VIQ_RTK)) {
              TypeReference<ArrayList<ArrayList<String>>> type_ref = new TypeReference<ArrayList<ArrayList<String>>>() {};
              Map<String, Object> payload = json_mapper.readValue(json_data, new TypeReference<Map<String,Object>>() {});
              ArrayList<ArrayList<String>> data = json_mapper.convertValue(payload.get("data"), type_ref);
              int k_value = (int) payload.get("k_value");
              int n_threads = (int) payload.get("n_threads");
              System.out.println("k_value: "+k_value);
              System.out.println("n_threads: "+n_threads);
              ArrayList<ArrayList<Integer>> vulnerabilities = identify_vulnerabilities(data,2,2);
              String json_vulnerabilities = json_mapper.writeValueAsString(vulnerabilities);
              channel.basicPublish(server.rabbitmq_exchange_name, server.PYTHON_VIQ_RTK, null, json_vulnerabilities.getBytes());
            }

          } catch (JsonProcessingException e) {
            e.printStackTrace();
          }
        }
      }.withServer(this);

      for(String queue : this.QUEUES) {
        channel.basicConsume(queue,true,consumer);
      }
    } catch (IOException e) {
      e.printStackTrace();
    } 
  }
  

  public static void main(String[] args) {
    Server server = new Server();
    server.run();
  }

  public ArrayList<String> identify_type(ArrayList<ArrayList<String>> samples) {
    TypeIdentifier t_identifier = new TypeIdentifier();
    ArrayList<String> data_types = new ArrayList();
    for(ArrayList<String> sample: samples) {
      data_types.add(t_identifier.identify_type(sample));
    }
    return data_types;
  }
  
  public ArrayList<ArrayList<Integer>> identify_vulnerabilities(ArrayList<ArrayList<String>> dataset,int uniqueness_threshold,int n_threads) {
    List<List<String>> list_dataset = new ArrayList<List<String>>(dataset);
    System.out.println("converted dataset");
    VulnerabilitiesIdentifier v_identifier = new VulnerabilitiesIdentifier(list_dataset);
    return v_identifier.identify_vulnerabilities(uniqueness_threshold,n_threads, DUCC.Strategy.DESCENDING);
  }
}


