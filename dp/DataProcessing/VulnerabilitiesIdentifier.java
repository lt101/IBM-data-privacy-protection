
package DataProcessing;

import com.ibm.research.drl.dpt.IPVAlgorithm;
import com.ibm.research.drl.dpt.datasets.IPVDataset;
import com.ibm.research.drl.dpt.vulnerability.IPVVulnerability;
import com.ibm.research.drl.dpt.vulnerability.ducc.*;
import com.ibm.research.drl.dpt.vulnerability.ducc.DUCC.Strategy;
import com.ibm.research.drl.dpt.generators.ItemSet;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.LinkedList;



public class VulnerabilitiesIdentifier {
    
    public IPVDataset dataset;
    
    public VulnerabilitiesIdentifier(List<List<String>> dataset) {
        this.dataset = new IPVDataset(dataset, null, false);
    }

    public ArrayList<ArrayList<Integer>> identify_vulnerabilities(int uniqueness_threshold,int n_threads, DUCC.Strategy strategy) {
        IPVAlgorithm ipv_algorithm = new DUCC(n_threads, strategy, uniqueness_threshold);
        Collection<IPVVulnerability> vulnerabilities_collection = ipv_algorithm.apply(this.dataset);
        ArrayList<ArrayList<Integer>> vulnerabilities_list = new ArrayList<>();
        for(IPVVulnerability vulnerability: vulnerabilities_collection) {
            ArrayList<Integer> item_list = new ArrayList<>();
            for(Integer item: vulnerability.getItemSet().getItems()) {
                item_list.add(item);
            }
            vulnerabilities_list.add(item_list);
        }
        return vulnerabilities_list;

    }


}
