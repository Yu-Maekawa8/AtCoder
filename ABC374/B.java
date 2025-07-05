// AC済み問題: abc374_b
// 提出日時: 2024-10-20 15:26:30
// 実行時間: 68ms
// 注意: AtCoderは public class Main だが、IDE用に public class B に変更

package ABC374;

import java.util.*;
public class B{
    public static void main(String [] args){
        Scanner sc = new Scanner(System.in);
        List<String> s1 = new ArrayList<>(Arrays.asList(sc.nextLine().split("")));
        List<String> s2 = new ArrayList<>(Arrays.asList(sc.nextLine().split("")));
        int answer = 1;
        int i =0;
        
        while(s1.size() != s2.size()){
          if(s1.size() < s2.size()){
            s1.add("nothing");
          }else{
            s2.add("nothing");
          }
        }  
        
        for(i = 0 ; i < s1.size() ; i++){
            if(!s1.get(i).equals(s2.get(i))){
                answer = i+1;
                break;
            }else{}
        }
        if(i == s1.size()){
          answer = 0;
        }
        System.out.println(answer);
    }
}