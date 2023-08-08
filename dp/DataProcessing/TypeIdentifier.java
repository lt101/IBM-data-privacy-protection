/* 
Author : Raphaël Lasalle
Date : 07-03-2023
 */

 package DataProcessing;

import com.ibm.research.drl.dpt.providers.ProviderType;
import com.ibm.research.drl.dpt.providers.identifiers.IdentifierFactory;
import com.ibm.research.drl.dpt.providers.identifiers.Identifier;
 
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;

import javax.print.DocFlavor.STRING;

public class TypeIdentifier {

    final String IDENFITIERS_FILE_PATH = "ressources/identifiers.properties";
    final String NULL_TYPE = "NULL";
    final String GENERIC_TEXT_TYPE = "TEXT";
    final String GENERIC_NUMBER_TYPE = "NUMBER";
    final String NUMERICAL_REGEX = "^\\s*-?\\d+(\\s?\\d+)*(\\.\\d+)?\\s*$";
    public File file;
    public FileInputStream input;
    public IdentifierFactory identifier_factory;
    public Collection<Identifier> identifiers;

    public TypeIdentifier() {
        
        try {
            this.file = new File(this.IDENFITIERS_FILE_PATH);
            this.input = new FileInputStream(this.file);
            this.identifier_factory = new IdentifierFactory(this.input);
            this.identifiers = this.identifier_factory.availableIdentifiers();
          }
          catch (Exception e) {
            System.out.println("type identifier file could not be found");
          }
    }

    public String identify_type(ArrayList<String> sample) {

      ArrayList<String> types = new ArrayList<>();
      for(String data_point:sample) {
        for (Identifier identifier: identifiers) {
          boolean match = identifier.isOfThisType(data_point);
          if (match == true) {
              types.add(identifier.getType().name());
              continue;
          }
        
        }

      }
      HashMap<String, Integer> frequencies = new HashMap<String, Integer>();

      for (String type : types) {
        if (frequencies.containsKey(type)) {
            frequencies.put(type, frequencies.get(type) + 1);
        } else {
            frequencies.put(type, 1);
        }
      }

      
      String most_frequent_type = null;
      int max_count = 0;
      for (Map.Entry<String, Integer> entry : frequencies.entrySet()) {
          if (entry.getValue() > max_count) {
              most_frequent_type = entry.getKey();
              max_count = entry.getValue();
          }
      }
      
      if(is_numerical(sample) && most_frequent_type==null) {
        return GENERIC_NUMBER_TYPE;
      }

      if(!is_numerical(sample) && most_frequent_type==null) {
        return GENERIC_TEXT_TYPE;
      }

      return most_frequent_type;
    }

    Boolean is_numerical(ArrayList<String> list) {
      Pattern numerical_pattern = Pattern.compile(NUMERICAL_REGEX);
      int index = 0;
      int null_count = 0;
      for(String element:list) {
        if(element==null) {
          null_count++;
        } 
        else if(!numerical_pattern.matcher(element).matches() || null_count==list.size()) {
          return false;
        }
        if(null_count==list.size()) {
          return false;
        }
        index++;
      }
      return true;
      
    }

    public static void main(String[] args) {
        
      }
    
}
