#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <map>
#include <utility>
//chrono included to test how long it takes to build a tree to ensure a timeout won't occur
#include <chrono>

struct TreeNode;
struct EdgeNode;
typedef std::string tree_t;
 
struct EdgeNode{
    tree_t val;
    TreeNode* subtree;
    EdgeNode* next;
};
 
struct TreeNode{
    tree_t val;
    EdgeNode* subtree_l;
};

// Allocates a new TreeNode with given value
TreeNode* allocate_tree_node(tree_t e){
    TreeNode* tmp = new TreeNode;
    tmp->val = e;
    tmp->subtree_l = NULL;
    return tmp;
}

// Constructs a new EdgeNode that links to a subtree
EdgeNode* cons_edge_node(TreeNode* t, tree_t val, EdgeNode* subtree_l){
    EdgeNode* tmp = new EdgeNode;
    tmp->subtree = t;
    tmp->next = subtree_l;
    tmp->val = val;
    return tmp;
}

// Creates the root of a tree with the specified value
TreeNode* build_tree_root(tree_t e){
    return allocate_tree_node(e);
}

/// this function returns the number of nodes in the tree (whose root is) t
/// (see also example of expected output below)
int count_nodes(TreeNode* t){
    int count=0;
    EdgeNode* tmp;
    if(t == NULL){
        return 0;
    }
    count += 1;
    tmp = t->subtree_l;
    while(tmp != NULL){
        count += count_nodes(tmp->subtree);
        tmp = tmp->next;
    }
    return count;
}

/// this function returns the number of leaf nodes in the tree (whose root is) t
/// (see also example of expected output below)
int count_leaf_nodes(TreeNode* t){
    int count=0;
    EdgeNode* tmp;
    if(t == NULL){
        return 0;
    }
    else if(t->subtree_l == NULL){
        return 1;
    }
    tmp = t->subtree_l;
    while (tmp != NULL){
        count += count_leaf_nodes(tmp->subtree);
        tmp = tmp->next;
    }
    return count;
}

/// this function deallocates *all* the memory (dynamically) allocated for the tree
/// this will include instances of the structured data type TreeNode
/// and instances of the structured data type EdgeNode
void deallocate_tree(TreeNode* t){
    if(t == NULL){
        return;
    }
    EdgeNode* currentEdge=t->subtree_l;
    EdgeNode* nextEdge;
    while(currentEdge != NULL){
        nextEdge = currentEdge->next;
        deallocate_tree(currentEdge->subtree);
        delete(currentEdge);
        currentEdge = nextEdge;
    } 
    delete t;
}

//checks if all the elements in a vector are equal returns true if they are and false if they aren't
bool all_equal(const std::vector<tree_t>& input){

    if (input.size() < 2) {
        return true;
    }

    for(int i = 0; i < input.size()-1; i++){
        if(input[i] != input[i+1]){
            return false;
        }
    }
    return true;
}

//for a given treenode checks if the value of all the subtree's of each edgenode are the same
//returns the first value in the vector always if they are the same passes by refrence true  
//if they aren't passes by refrence false
tree_t check_constant(TreeNode* t, bool& check){
    EdgeNode* currentEdge = t->subtree_l;
    std::vector<tree_t> output;

    while(currentEdge != NULL){
        output.push_back((currentEdge->subtree)->val);
        currentEdge = currentEdge->next;
    }
    if(all_equal(output) && output.size() > 0){
        check = true;
        return output[0];
    }

    check = false;
    //function must return something even if the condition is false, I assume here that the tree is always made of strings
    return "No";
}

//checks if the tree node with root t has a non-null subtree returns true if it is non-null
//returns false otherwise
bool depth_check(TreeNode* t){
    if(t->subtree_l == NULL){
        return false;
    }
    return true;
}

//returns pointers to the ends of the tree where the ends of the tree are defined as the
//first tree node before each output node in the tree
std::vector<TreeNode*> ends_of_tree(TreeNode* t){
    EdgeNode* current_edge = t->subtree_l;
    TreeNode* current_tree = t;
    std::vector<TreeNode*> output, output_partial;

    if(!depth_check(t)){
        return output;
    }
    if(current_tree->subtree_l->subtree->subtree_l == NULL){
        output.push_back(current_tree);
        return output;
    }
    else{
        while(current_edge != NULL){
            output_partial = ends_of_tree(current_edge->subtree);
            output.insert(output.end(), output_partial.begin(), output_partial.end());
            current_edge = current_edge->next;
        }
    }
    return output;
}

//deallocates the tree from t onwards except for the given tree node t
void deallocate_sub_tree(TreeNode* t){
    if(t == NULL){
        return;
    }
    EdgeNode* currentEdge=t->subtree_l;
    EdgeNode* nextEdge;
    while(currentEdge != NULL){
        nextEdge = currentEdge->next;
        deallocate_tree(currentEdge->subtree); 
        delete(currentEdge);
        currentEdge = nextEdge;
    } 
}

//reorganizes the tree based on if we have ends of the tree with constant values for the output
//nodes in order to remove redundant information from the tree
void reorganize_tree(TreeNode* t){
    TreeNode* current = t;
    tree_t val;
    bool check;

    val = check_constant(current,check);
    if(check){
        val = check_constant(current,check);
        current->val = val;
        deallocate_sub_tree(current);
        current->subtree_l = NULL;
    }
}

//looks for the specified element in the vector and returns -1 if it is not in the list
int find_in_vector(const std::vector<tree_t>& input,tree_t e){
    for(int i = 0; i<input.size(); i++){
        if(e == input[i]){
            return i;
        }
    }
    return -1;
}

//counts the frequency of each element in the list
std::vector<int> vector_elements_count(const std::vector<tree_t>& input){
    std::vector<int> output;
    std::vector<tree_t> output_names;
    int position;

    for(int i = 0; i<input.size(); i++){
        position = find_in_vector(output_names, input[i]);
        if(position == -1){
            output.push_back(1);
            output_names.push_back(input[i]);
        }
        else{
            output[position] += 1;
        }
    }

    return output;
}

//adds all the integer values in the vector together
int add_all(const std::vector<int>& input){
    int output = 0;

    for(int i = 0; i < input.size(); i++){
        output += input[i];
    }

    return output;
}

//calculates the entropy of a given node, where the frequency of each output is represented
//as a vector
double entropy(const std::vector<int>& input){
    double output = 0;
    int sum = add_all(input);

    for(int i = 0; i<input.size(); i++){
        output += -(double(input[i])/sum)*(logb(double(input[i])/sum));
    }

    return output;
}

//prints out a vector
void print_vector(const std::vector<tree_t>& input){
    for(int i = 0; i<input.size(); i++){
        std::cout << input[i] <<std::endl;
    }
}

//calculates the info gain of each column in the input vector and return a vector of doubles
//which contains the info gain of each column in the same order the columns are given in 
std::vector<double> node_info_gain(const std::vector<std::vector<tree_t>>& input){
    
    std::vector<tree_t> columns = input[0], results, current_store;
    std::vector<int> results_count;
    std::vector<double> output;
    int position;
    std::map<tree_t, std::vector<tree_t>> mp;
    double parent_entropy, child_entropy, current_info_gain;

    columns.pop_back();

    //add all outputs to the results vector and count how many of each result there is calculate the entropy of the parent node
    for(int i = 1; i<input.size(); i++){
        results.push_back(input[i].back());
    }
    results_count = vector_elements_count(results);
    parent_entropy = entropy(results_count);

    //iterate through the input vector column by column and row by row
    for(int i = 0; i<input[0].size()-1; i++){
        
        //calculate child entropy, we use a map to store the decisions made by each node and map them to their corresponding output
        child_entropy = 0;
        current_store.clear();
        mp.clear();
        for(int c = 1; c<input.size(); c++){
            current_store.push_back(input[c][i]);
        }
        for(int c = 0; c<current_store.size(); c++){
            mp[current_store[c]].push_back(results[c]);
        }

        //we find the total weighted sum
        for(auto i = mp.begin(); i != mp.end(); i++){            
            child_entropy += (double((i->second).size())/results.size())*entropy(vector_elements_count(i->second));
        }

        current_info_gain = parent_entropy-child_entropy;
        output.push_back(current_info_gain);
    }

    return output;
}

//uses bubble sort to reorder the input vector at the same time as the info vector in decreasing order
void reorder_list(std::vector<double>& info, std::vector<std::vector<tree_t>>& input){
    int i, j;

    for (i = 0; i < info.size()-1; i++) {
        for (j = 0; j < info.size()-i-1; j++) {
            if (info[j] < info[j + 1]) {            
                std::swap(info[j], info[j + 1]);
                for(int c = 0; c<input.size(); c++){
                    std::swap(input[c][j], input[c][j+1]);
                }
            }
        }

    }
}

class A3Tree{ 
public:

    A3Tree(const std::vector<std::vector<tree_t>> input){

        columns = input[0];
        std::vector<double> info = node_info_gain(input);
        std::vector<std::vector<tree_t>> input_copy = input;
        int count_before=-1, count_after=0;
        reorder_list(info, input_copy);

        t = build_tree_root(input_copy[0][0]);
        TreeNode* tmp = t;

        for(int c = 1; c<input_copy.size(); c++){
            tmp = t;

            for(int i = 0; i<input_copy[0].size() - 1; i++){
                if( i != input_copy[0].size()-2 ){
                    tmp = find_or_create_node(tmp, input_copy[c][i], input_copy[0][i+1]);
                }
                else{
                    tmp = find_or_create_node(tmp, input_copy[c][i], input_copy[c][i+1]);
                }
            }
        }

        while(count_before != count_after){

            count_before = count_nodes(t);
            std::vector<TreeNode*> tree_ends = ends_of_tree(t);

            for(int i = 0; i<tree_ends.size(); i++){
                reorganize_tree(tree_ends[i]);
            }

            count_after = count_nodes(t);
        }
        
    }

    //prints tree
    void print_treeA() const {

        print_tree(t);

    }

    //looks for an edgenode starting from treenode t and returns a pointer to it, if it can't find the
    //edge creates it and the corresponding treenode with the values of column and adds it to the tree, 
    //then returns pointer to the new treenode
    TreeNode* find_or_create_node(TreeNode* parent, const tree_t& value, const tree_t& column) {

        EdgeNode* edge = parent->subtree_l;
        
        while(edge != NULL){
            if(edge->val == value){
                return edge->subtree;
            }
            edge = edge->next;
        }

        TreeNode* newNode = allocate_tree_node(column);
        EdgeNode* newEdge = cons_edge_node(newNode, value, NULL);
        newEdge->next = parent->subtree_l;
        parent->subtree_l = newEdge;
        return newNode;
    }   

    //queries the decision tree using a vector
    tree_t query(std::vector<tree_t> query){

        std::map<tree_t, tree_t> mp;
        for(int i=0; i<query.size(); i++){
            mp[columns[i]] = query[i];
        }

        TreeNode* current_tree_node = t;
        bool found;
        EdgeNode* current_edge_node;

        for(int i=0; i<query.size(); i++){
            found = false;
            current_edge_node = current_tree_node->subtree_l;

            if(current_edge_node == NULL){
                return current_tree_node->val;
            }   

            while(current_edge_node != NULL && found == false){
                if(current_edge_node->val == query[i] && mp[current_tree_node->val] == query[i]){
                    found = true;

                    current_tree_node = current_edge_node->subtree;
                    query.erase(query.begin()+i);
                    i = -1;
                }
                current_edge_node = current_edge_node->next;
            }
        }
        return current_tree_node->val;
    }

    //returns pointer to the root of the tree 
    TreeNode* returnRoot(){
        return t;
    }

    ~A3Tree(){
        deallocate_tree(t);
    }

private:
 
    TreeNode* t;
    // member data pointing to the root of the tree
    // do not change the name or anything else regarding
    // this member data declaration
    std::vector<tree_t> columns;

    //prints the tree, const keyword used at the end here as it does not change anything about the object
    //we define a default value for depth in the function, so it can be easily used recursively incrementing
    //with each recursion
    void print_tree(const TreeNode* node, int depth = 0) const {
        if (node == NULL) {
            return;
        }

        std::string indent(depth * 4, ' '); 
        std::cout << indent << node->val << std::endl;

        EdgeNode* edge = node->subtree_l;
        while (edge != NULL) {
            std::cout << indent << " -> " << edge->val << ": " << std::endl;
            print_tree(edge->subtree, depth + 1);
            edge = edge->next;
        }
    }
    
};

int main(){

    const auto& start = std::chrono::steady_clock::now();
    std::vector<std::vector<std::string>> input1
    {
        {"temperature", "rain", "wind", "quality"},
        {"high", "yes", "light", "acceptable"},
        {"low", "yes", "light", "acceptable"},
        {"low", "no", "moderate", "good"},
        {"high", "yes", "strong", "poor"},
        {"high", "yes", "moderate", "acceptable"},
        {"high", "no", "moderate", "good"},
        {"low", "yes", "strong", "poor"},
        {"high", "no", "light", "good"},
        {"low", "yes", "moderate", "poor"},
        {"high", "no", "strong", "poor"}
    };
 
    std::vector<std::vector<std::string>> input2
    {
        {"Feature_3", "feature2", "feature", "feature0", "not_a_feature"},
        {"a13480", "10", "a13480", "a", "1"},
        {"B_34203", "B_34203", "1343432", "a", "2"},
        {"a13480", "8", "57657", "a", "3"},
        {"B_34203", "9", "4523", "a", "a2"},
        {"B_34203", "6", "4523", "a", "some_value"},
        {"a13480", "5", "4523", "a", "1"}
    };

    std::vector<std::vector<std::string>> test1 {
        {"Color", "Shape", "Material", "Quality"},
        {"Red", "Square", "Plastic", "Good"},
        {"Blue", "Circle", "Metal", "Poor"},
        {"Green", "Triangle", "Wood", "Excellent"}
    };

    std::vector<std::vector<std::string>> test2 {
        {"Temperature", "Wind", "Rain", "Outcome"},
        {"High", "Strong", "Yes", "Bad"},
        {"High", "Strong", "No", "Good"},
        {"Low", "Weak", "No", "Good"}
    };
    //std::vector<double> out;
    std::vector<std::vector<std::string>> test3 {
        {"Grade", "Age", "Subject", "Performance"},
        {"Senior", "Old", "Math", "Pass"},
        {"Junior", "Young", "Science", "Fail"},
        {"Senior", "Old", "Science", "Pass"}
    };

    std::vector<std::vector<std::string>> test4 {
        {"Grade", "Age", "Subject", "Performance"},
        {"Senior", "Old", "Science", "Pass"}
    };

    A3Tree t1(input1);
    A3Tree t2(input2);
    A3Tree t3(test1);
    A3Tree t4(test2);
    A3Tree t5(test3);
    A3Tree t6(test4);

    t1.print_treeA();
    t2.print_treeA();
    t3.print_treeA();
    t4.print_treeA();
    t5.print_treeA();
    t6.print_treeA();
    
    std::cout<<"End of tree printing"<<std::endl;
    std::vector<std::string> query1 {"Senior", "Old", "Science"};
    std::vector<std::string> query2 {"Senior", "Old", "Science"};
    std::cout << t5.query(query1) << std::endl;
    std::cout << t6.query(query2) << std::endl;
    //TreeNode* tst;
    //tst = (t1.returnRoot());
    //std::cout<<tst->subtree_l->next->subtree->subtree_l->subtree->subtree_l->val<<std::endl;
    //std::cout<< check_constant(tst->subtree_l->next->subtree->subtree_l->subtree)<<std::endl;
    //std::cout<< ends_of_tree(tst).size() << std::endl;
    //std::cout << "Finding ends of tree" << std::endl;
    //std::vector<TreeNode*> tree_ends = ends_of_tree(tst);
    //std::cout << "Ends of tree found" << std::endl;
    //out = node_info_gain(input1);
    //for(int i = 0; i<out.size(); i++){
    //    std::cout << out[i] <<std::endl;
    //}

    std::vector<std::string> q;
 
    q =  {"high", "yes", "moderate"};
    std::cout << t1.query(q) << std::endl;
    // this should print: acceptable
 
    q = {"B_34203", "9", "1343432", "a"};
    std::cout << t2.query(q) << std::endl;
    // this should print: a2
    auto end = std::chrono::steady_clock::now();
    auto diff = end-start;
    std::cout << std::chrono::duration<double, std::milli>(diff).count() << "ms" << std::endl;
    std::cout << count_leaf_nodes(t2.returnRoot());
    
}
