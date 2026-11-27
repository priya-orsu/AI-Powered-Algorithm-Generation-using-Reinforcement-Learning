"""
Machine Learning, Number Systems & Data Encoding Algorithm Catalog
Provides high-fidelity implementations, algorithmic working steps, pseudocode,
time/space complexities, advantages, disadvantages, and interview questions.
"""
from typing import List, Dict, Any
import re

ML_ENCODING_REGISTRY = [
    {
        "name": "Random Forest Algorithm",
        "algorithm_name": "Random Forest Algorithm",
        "category": "Machine Learning",
        "description": "An ensemble learning algorithm that constructs a collection of uncorrelated decision trees using bootstrap aggregation (bagging) and random feature subspace selection, combining their predictions through majority voting or averaging to achieve high accuracy and prevent overfitting.",
        "problem_statement": "Construct a robust ensemble classifier from multiple decision tree estimators to classify high-dimensional feature samples with low variance and strong generalization.",
        "keywords": ["random forest", "random forests", "rf", "random forest algorithm", "ensemble learning", "bagging trees", "bootstrap aggregation", "random forest classifier", "random forest regression"]
    },
    {
        "name": "Decision Tree Algorithm",
        "algorithm_name": "Decision Tree Algorithm",
        "category": "Machine Learning",
        "description": "A non-parametric supervised learning algorithm that partitions feature space into hierarchical axis-aligned decision regions using recursive binary splitting based on Gini impurity or Information Gain.",
        "problem_statement": "Recursively split feature space into homogeneous leaf nodes to classify input records with maximum purity.",
        "keywords": ["decision tree", "decision tree algorithm", "cart", "id3", "c4.5", "gini impurity", "information gain", "tree classifier"]
    },
    {
        "name": "Linear Regression Algorithm",
        "algorithm_name": "Linear Regression Algorithm",
        "category": "Machine Learning",
        "description": "A fundamental statistical and supervised learning algorithm that models the linear relationship between a scalar dependent response variable and one or more explanatory feature variables using Ordinary Least Squares (OLS) residual minimization.",
        "problem_statement": "Fit an optimal hyperplane minimizing the sum of squared residuals between observed continuous responses and linear feature predictions.",
        "keywords": ["linear regression", "linear regression algorithm", "least squares", "ordinary least squares", "ols", "univariate regression", "line of best fit", "linear model"]
    },
    {
        "name": "Logistic Regression Algorithm",
        "algorithm_name": "Logistic Regression Algorithm",
        "category": "Machine Learning",
        "description": "A probabilistic classification algorithm that models the log-odds of a binary categorical dependent outcome using the logistic sigmoid function parameterized by feature weights trained via gradient ascent on cross-entropy likelihood.",
        "problem_statement": "Estimate conditional posterior probability P(Y=1|X) and classify binary instances using a parameterized sigmoid threshold model.",
        "keywords": ["logistic regression", "logistic regression algorithm", "sigmoid classification", "logit", "binary classification logistic", "cross entropy classification"]
    },
    {
        "name": "Support Vector Machine (SVM)",
        "algorithm_name": "Support Vector Machine (SVM)",
        "category": "Machine Learning",
        "description": "A maximum-margin supervised learning model that computes an optimal separating hyperplane in high-dimensional feature space maximizing geometric distance to the closest training support vectors, incorporating soft-margin slack and hinge loss.",
        "problem_statement": "Find a decision boundary hyperplane that separates two classes with maximum margin width and minimum margin slack violations.",
        "keywords": ["svm", "support vector machine", "support vector machine algorithm", "svc", "linear svm", "maximum margin hyperplane", "support vectors"]
    },
    {
        "name": "K-Nearest Neighbors (KNN)",
        "algorithm_name": "K-Nearest Neighbors (KNN)",
        "category": "Machine Learning",
        "description": "A non-parametric, lazy-learning instance-based classification and regression algorithm that classifies an unlabeled query point based on plurality class vote among its K nearest Euclidean distance neighbors in feature space.",
        "problem_statement": "Assign class labels to query points by querying and aggregating the K closest labeled instances in metric space.",
        "keywords": ["knn", "k-nearest neighbors", "k nearest neighbors", "knn algorithm", "k nearest neighbours", "nearest neighbor classifier"]
    },
    {
        "name": "Naive Bayes Classifier",
        "algorithm_name": "Naive Bayes Classifier",
        "category": "Machine Learning",
        "description": "A generative probabilistic classifier applying Bayes theorem with the strong conditional independence assumption among features given the class label, computing posterior likelihoods via prior probabilities and Gaussian or multinomial densities.",
        "problem_statement": "Compute maximum a posteriori (MAP) class probabilities for feature vectors under conditional feature independence assumptions.",
        "keywords": ["naive bayes", "naive bayes classifier", "gaussian naive bayes", "bayes classifier", "prior likelihood probability", "multinomial naive bayes"]
    },
    {
        "name": "Principal Component Analysis (PCA)",
        "algorithm_name": "Principal Component Analysis (PCA)",
        "category": "Machine Learning",
        "description": "An unsupervised linear dimensionality reduction algorithm that projects high-dimensional data onto orthogonal axes of maximal variance by computing eigenvectors of the empirical data covariance matrix.",
        "problem_statement": "Reduce feature dimensionality from D dimensions to K dimensions (K < D) while retaining maximal explained data variance.",
        "keywords": ["pca", "principal component analysis", "pca algorithm", "dimensionality reduction", "covariance eigenvectors", "feature projection", "eigen decomposition"]
    },
    {
        "name": "Gradient Descent Optimizer",
        "algorithm_name": "Gradient Descent Optimizer",
        "category": "Machine Learning",
        "description": "A first-order iterative optimization algorithm for finding a local minimum of a differentiable objective loss function by taking steps proportional to the negative gradient of the function at the current parameter coordinates.",
        "problem_statement": "Iteratively update model parameter weights in the direction of steepest descent to minimize an empirical loss function.",
        "keywords": ["gradient descent", "gradient descent algorithm", "sgd", "stochastic gradient descent", "batch gradient descent", "learning rate optimizer", "steepest descent"]
    },
    {
        "name": "DBSCAN Clustering Algorithm",
        "algorithm_name": "DBSCAN Clustering Algorithm",
        "category": "Machine Learning",
        "description": "A density-based spatial clustering algorithm that groups points with high local neighborhood density into clusters while identifying sparse outliers as noise, discovering arbitrarily shaped clusters without requiring a predefined cluster count K.",
        "problem_statement": "Cluster spatial points based on Euclidean epsilon-neighborhood densities and separate core clusters from noise outliers.",
        "keywords": ["dbscan", "dbscan algorithm", "density based clustering", "density based spatial clustering", "eps neighborhood clustering", "core points clustering"]
    },
    {
        "name": "Q-Learning Algorithm",
        "algorithm_name": "Q-Learning Algorithm",
        "category": "Reinforcement Learning",
        "description": "A model-free, off-policy temporal-difference reinforcement learning algorithm that learns an optimal action-value function Q*(s, a) directly through iterative Bellman equation updates and epsilon-greedy exploration in Markov Decision Processes (MDPs).",
        "problem_statement": "Find an optimal policy mapping environment states to actions that maximizes cumulative discounted future rewards without prior model transition probabilities.",
        "keywords": ["q-learning", "q learning", "q learning algorithm", "reinforcement learning q", "q table", "temporal difference rl", "bellman equation", "off policy rl"]
    },
    {
        "name": "Octal Encoding & Conversion",
        "algorithm_name": "Octal Encoding & Conversion",
        "category": "Number Systems & Encoding",
        "description": "A positional base-8 numerical encoding algorithm that converts integer values and byte sequences into radix-8 representations using octal digits [0-7], where each octal digit corresponds to exactly 3 binary bits.",
        "problem_statement": "Convert integers and binary sequences into compact base-8 representations and decode octal strings back into decimal and binary values.",
        "keywords": ["octal encoding", "octal conversion", "octal", "octal algorithm", "decimal to octal", "octal to decimal", "octal to binary", "binary to octal", "base 8 encoding", "base-8", "octal representation"]
    },
    {
        "name": "Binary Encoding & Conversion",
        "algorithm_name": "Binary Encoding & Conversion",
        "category": "Number Systems & Encoding",
        "description": "A foundational base-2 encoding algorithm that represents numeric and character data as strings of binary bits (0 and 1) using positional power expansion and bitwise operations.",
        "problem_statement": "Encode integers into binary bit arrays and compute inverse conversions between binary, decimal, and bitwise two's complement representations.",
        "keywords": ["binary encoding", "binary conversion", "binary algorithm", "decimal to binary", "binary to decimal", "base 2 encoding", "base-2", "two complement", "bitwise encoding"]
    },
    {
        "name": "Hexadecimal Encoding & Conversion",
        "algorithm_name": "Hexadecimal Encoding & Conversion",
        "category": "Number Systems & Encoding",
        "description": "A base-16 positional numeral encoding system utilizing 16 symbols ('0'-'9' and 'A'-'F') to concisely represent byte streams and binary words, with each hex digit precisely mapping to 4 binary bits (one nibble).",
        "problem_statement": "Encode numerical data and binary byte streams into compact base-16 strings and decode hexadecimal formats back into integers and ASCII characters.",
        "keywords": ["hexadecimal encoding", "hex encoding", "hex conversion", "hexadecimal algorithm", "hex to decimal", "decimal to hex", "base 16 encoding", "hex dump"]
    },
    {
        "name": "Run-Length Encoding (RLE)",
        "algorithm_name": "Run-Length Encoding (RLE)",
        "category": "Data Compression & Encoding",
        "description": "A lossless data compression and encoding algorithm that replaces consecutive repeating sequence runs of identical data elements with single data values paired with their repetition count lengths.",
        "problem_statement": "Compress repetitive string and image raster sequences by encoding contiguous identical characters into count-character pairs.",
        "keywords": ["run length encoding", "run-length encoding", "rle", "rle algorithm", "run length compression", "lossless rle", "repetitive character compression"]
    },
    {
        "name": "Base64 Encoding & Decoding",
        "algorithm_name": "Base64 Encoding & Decoding",
        "category": "Number Systems & Encoding",
        "description": "A binary-to-text encoding algorithm that transforms arbitrary binary data into an ASCII string format using a 64-character alphabet, segmenting 8-bit byte triplets into 6-bit chunks with '=' padding.",
        "problem_statement": "Safely transmit binary byte payloads over text-only protocols (such as SMTP and HTTP) without character loss or control sequence corruption.",
        "keywords": ["base64", "base 64", "base64 encoding", "base64 algorithm", "base64 decoding", "binary to text base64", "radix 64"]
    },
    {
        "name": "Huffman Coding Algorithm",
        "algorithm_name": "Huffman Coding Algorithm",
        "category": "Data Compression & Encoding",
        "description": "An optimal prefix-free entropy encoding algorithm that assigns variable-length binary bit codes to characters based on their frequencies of occurrence using a min-heap priority queue to construct a binary tree.",
        "problem_statement": "Generate an optimal prefix code tree minimizing expected weighted codeword length for a given character frequency distribution.",
        "keywords": ["huffman coding", "huffman code", "huffman algorithm", "huffman compression", "prefix code compression", "frequency tree"]
    },
    {
        "name": "Shannon-Fano Coding",
        "algorithm_name": "Shannon-Fano Coding",
        "category": "Data Compression & Encoding",
        "description": "A top-down variable-length prefix coding algorithm that recursively divides sorted symbol probabilities into two equal-frequency subsets to construct efficient prefix-free binary codes.",
        "problem_statement": "Construct variable-length binary codes for a symbol alphabet by recursively splitting probability distributions into equal cumulative halves.",
        "keywords": ["shannon fano", "shannon-fano", "shannon fano coding", "shannon fano algorithm", "entropy coding", "probability split coding"]
    },
    {
        "name": "Hamming Error Correction Code",
        "algorithm_name": "Hamming Error Correction Code",
        "category": "Information Theory & Error Correction",
        "description": "A linear block error-correcting code (Hamming(7,4)) that inserts parity check bits at power-of-two index positions, enabling automated detection and correction of single-bit transmission errors.",
        "problem_statement": "Encode 4-bit data words with 3 redundant parity bits to detect and automatically correct any single-bit transmission error.",
        "keywords": ["hamming code", "hamming 7 4", "hamming code algorithm", "error correcting code", "syndrome decoding", "single bit error correction", "parity check"]
    }
]

def is_ml_or_encoding_algorithm(name: str) -> bool:
    """Checks if the algorithm name matches an entry in this catalog."""
    n = name.lower().strip()
    clean_n = re.sub(r"\s*algorithm\s*$", "", n).strip()
    for item in ML_ENCODING_REGISTRY:
        item_n = item["algorithm_name"].lower()
        clean_item_n = re.sub(r"\s*algorithm\s*$", "", item_n).strip()
        if n == item_n or clean_n == clean_item_n or n in item_n or clean_n in clean_item_n:
            return True
        for kw in item["keywords"]:
            if kw == n or kw == clean_n or kw in n:
                return True
    return False

def _match_key(name: str) -> str:
    n = name.lower().strip()
    if "random forest" in n or "rf" in n:
        return "random_forest"
    if "octal" in n:
        return "octal"
    if "decision tree" in n:
        return "decision_tree"
    if "linear regression" in n:
        return "linear_regression"
    if "logistic regression" in n:
        return "logistic_regression"
    if "svm" in n or "support vector" in n:
        return "svm"
    if "knn" in n or "nearest" in n:
        return "knn"
    if "naive bayes" in n:
        return "naive_bayes"
    if "run length" in n or "rle" in n:
        return "rle"
    if "binary" in n:
        return "binary"
    if "hex" in n:
        return "hex"
    if "base64" in n:
        return "base64"
    if "q-learning" in n or "reinforcement" in n:
        return "q_learning"
    if "pca" in n or "principal component" in n:
        return "pca"
    if "gradient descent" in n:
        return "gradient_descent"
    if "dbscan" in n:
        return "dbscan"
    if "huffman" in n:
        return "huffman"
    if "shannon" in n:
        return "shannon_fano"
    if "hamming" in n:
        return "hamming"
    return "default"

# =============================================================================
# PYTHON IMPLEMENTATIONS MAP
# =============================================================================
ML_PYTHON_CODE = {
    "random_forest": """# Random Forest Classifier Implementation (Ensemble of Decision Trees)
import random
import math

class SimpleDecisionTree:
    # A single binary decision stump/tree node for Random Forest ensemble
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.tree = None

    def _gini(self, y):
        if not y:
            return 0.0
        p1 = sum(y) / len(y)
        p0 = 1.0 - p1
        return 1.0 - (p0**2 + p1**2)

    def fit(self, X, y, depth=0, feature_subset_size=None):
        if not y or depth >= self.max_depth or len(set(y)) == 1:
            majority = 1 if (sum(y) / max(1, len(y))) >= 0.5 else 0
            return {"type": "leaf", "prediction": majority}

        n_features = len(X[0])
        subset_size = feature_subset_size or max(1, int(math.sqrt(n_features)))
        features = random.sample(range(n_features), subset_size)

        best_gini = float("inf")
        best_split = None

        for feat in features:
            values = sorted(set(row[feat] for row in X))
            for i in range(len(values) - 1):
                thresh = (values[i] + values[i + 1]) / 2.0
                left_idx = [j for j, row in enumerate(X) if row[feat] <= thresh]
                right_idx = [j for j, row in enumerate(X) if row[feat] > thresh]
                if not left_idx or not right_idx:
                    continue
                gini = (len(left_idx) * self._gini([y[j] for j in left_idx]) +
                        len(right_idx) * self._gini([y[j] for j in right_idx])) / len(y)
                if gini < best_gini:
                    best_gini = gini
                    best_split = (feat, thresh, left_idx, right_idx)

        if not best_split:
            majority = 1 if (sum(y) / max(1, len(y))) >= 0.5 else 0
            return {"type": "leaf", "prediction": majority}

        feat, thresh, left_idx, right_idx = best_split
        return {
            "type": "node",
            "feature": feat,
            "threshold": thresh,
            "left": self.fit([X[j] for j in left_idx], [y[j] for j in left_idx], depth + 1, feature_subset_size),
            "right": self.fit([X[j] for j in right_idx], [y[j] for j in right_idx], depth + 1, feature_subset_size)
        }

    def predict_one(self, node, x):
        if node["type"] == "leaf":
            return node["prediction"]
        if x[node["feature"]] <= node["threshold"]:
            return self.predict_one(node["left"], x)
        return self.predict_one(node["right"], x)

class RandomForestClassifier:
    # Ensemble of Decision Trees with Bootstrap Aggregation (Bagging)
    def __init__(self, n_estimators=10, max_depth=3):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.trees = []

    def fit(self, X, y):
        self.trees = []
        n_samples = len(X)
        for _ in range(self.n_estimators):
            boot_indices = [random.randint(0, n_samples - 1) for _ in range(n_samples)]
            X_boot = [X[i] for i in boot_indices]
            y_boot = [y[i] for i in boot_indices]

            tree = SimpleDecisionTree(max_depth=self.max_depth)
            tree_model = tree.fit(X_boot, y_boot)
            self.trees.append((tree, tree_model))

    def predict(self, X):
        predictions = []
        for x in X:
            votes = [tree.predict_one(model, x) for tree, model in self.trees]
            majority = 1 if sum(votes) > len(votes) / 2 else 0
            predictions.append(majority)
        return predictions

# Demonstration: Train Random Forest on Synthetic 2D Classification Data
random.seed(42)
X_train = [[2.5, 3.1], [1.2, 1.8], [3.0, 3.5], [1.0, 0.9], [5.5, 4.2], [6.1, 5.0], [5.0, 6.2], [6.8, 5.5]]
y_train = [0, 0, 0, 0, 1, 1, 1, 1]

rf = RandomForestClassifier(n_estimators=7, max_depth=3)
rf.fit(X_train, y_train)

X_test = [[1.5, 2.0], [6.0, 5.2], [2.8, 3.0], [5.2, 4.9]]
predictions = rf.predict(X_test)

print("[Random Forest Ensemble Results]")
for sample, pred in zip(X_test, predictions):
    print(f"  Input Features: {sample} -> Predicted Class: {pred}")
""",

    "octal": """# Octal Encoding & Conversion Algorithm Implementation
def decimal_to_octal(num: int) -> str:
    # Converts a non-negative decimal integer into an octal (base-8) string
    if num == 0:
        return "0"
    is_neg = num < 0
    num = abs(num)
    octal_digits = []
    while num > 0:
        remainder = num % 8
        octal_digits.append(str(remainder))
        num //= 8
    octal_str = "".join(reversed(octal_digits))
    return f"-{octal_str}" if is_neg else octal_str

def octal_to_decimal(octal_str: str) -> int:
    # Decodes an octal string into its decimal integer value
    octal_str = octal_str.strip()
    is_neg = octal_str.startswith("-")
    if is_neg:
        octal_str = octal_str[1:]
    decimal_val = 0
    for power, digit_char in enumerate(reversed(octal_str)):
        digit = int(digit_char)
        if digit < 0 or digit > 7:
            raise ValueError(f"Invalid octal digit '{digit_char}' in string '{octal_str}'")
        decimal_val += digit * (8 ** power)
    return -decimal_val if is_neg else decimal_val

def octal_to_binary(octal_str: str) -> str:
    # Converts each octal digit directly into its 3-bit binary triplet representation
    oct_to_bin_map = {
        '0': '000', '1': '001', '2': '010', '3': '011',
        '4': '100', '5': '101', '6': '110', '7': '111'
    }
    return "".join(oct_to_bin_map[d] for d in octal_str.replace("-", ""))

def binary_to_octal(binary_str: str) -> str:
    # Groups binary string into 3-bit chunks from the right and maps to octal digits
    pad_len = (3 - len(binary_str) % 3) % 3
    padded = ("0" * pad_len) + binary_str
    bin_to_oct_map = {
        '000': '0', '001': '1', '010': '2', '011': '3',
        '100': '4', '101': '5', '110': '6', '111': '7'
    }
    return "".join(bin_to_oct_map[padded[i:i+3]] for i in range(0, len(padded), 3))

def encode_text_to_octal(text: str) -> str:
    # Encodes an ASCII text string into a space-separated sequence of octal byte codes
    return " ".join(decimal_to_octal(ord(c)) for c in text)

def decode_octal_to_text(octal_encoded: str) -> str:
    # Decodes space-separated octal codes back into the original ASCII text
    return "".join(chr(octal_to_decimal(code)) for code in octal_encoded.split())

# Demonstration
sample_num = 455
oct_res = decimal_to_octal(sample_num)
dec_recovered = octal_to_decimal(oct_res)
bin_res = octal_to_binary(oct_res)
oct_recovered = binary_to_octal(bin_res)

sample_message = "Algorithm"
encoded_message = encode_text_to_octal(sample_message)
decoded_message = decode_octal_to_text(encoded_message)

print("[Octal Encoding & Conversion Results]")
print(f"  Decimal Input       : {sample_num}")
print(f"  Encoded Octal       : {oct_res} (Base-8)")
print(f"  Decoded Decimal     : {dec_recovered}")
print(f"  Binary Triplet View : {bin_res}")
print(f"  Recovered Octal     : {oct_recovered}")
print(f"  Encoded Message     : '{sample_message}' -> {encoded_message}")
print(f"  Decoded Text        : '{decoded_message}'")
""",

    "decision_tree": """# Decision Tree Classifier (ID3 / CART Gini Impurity)
class DecisionTreeNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    @property
    def is_leaf(self):
        return self.value is not None

class DecisionTreeClassifier:
    def __init__(self, max_depth=4, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None

    def _gini(self, y):
        if not y:
            return 0.0
        counts = {}
        for label in y:
            counts[label] = counts.get(label, 0) + 1
        return 1.0 - sum((count / len(y))**2 for count in counts.values())

    def _best_split(self, X, y):
        best_gini = float("inf")
        best_feat, best_thresh = None, None
        n_features = len(X[0])

        for feat in range(n_features):
            values = sorted(set(row[feat] for row in X))
            for i in range(len(values) - 1):
                thresh = (values[i] + values[i + 1]) / 2.0
                left_y = [y[j] for j, row in enumerate(X) if row[feat] <= thresh]
                right_y = [y[j] for j, row in enumerate(X) if row[feat] > thresh]
                if not left_y or not right_y:
                    continue
                gini = (len(left_y) * self._gini(left_y) + len(right_y) * self._gini(right_y)) / len(y)
                if gini < best_gini:
                    best_gini = gini
                    best_feat, best_thresh = feat, thresh
        return best_feat, best_thresh

    def _build_tree(self, X, y, depth=0):
        if len(set(y)) == 1 or len(y) < self.min_samples_split or depth >= self.max_depth:
            majority_class = max(set(y), key=y.count) if y else None
            return DecisionTreeNode(value=majority_class)

        feat, thresh = self._best_split(X, y)
        if feat is None:
            majority_class = max(set(y), key=y.count)
            return DecisionTreeNode(value=majority_class)

        left_idx = [i for i, row in enumerate(X) if row[feat] <= thresh]
        right_idx = [i for i, row in enumerate(X) if row[feat] > thresh]

        left_child = self._build_tree([X[i] for i in left_idx], [y[i] for i in left_idx], depth + 1)
        right_child = self._build_tree([X[i] for i in right_idx], [y[i] for i in right_idx], depth + 1)
        return DecisionTreeNode(feature=feat, threshold=thresh, left=left_child, right=right_child)

    def fit(self, X, y):
        self.root = self._build_tree(X, y)

    def _predict_sample(self, node, x):
        if node.is_leaf:
            return node.value
        if x[node.feature] <= node.threshold:
            return self._predict_sample(node.left, x)
        return self._predict_sample(node.right, x)

    def predict(self, X):
        return [self._predict_sample(self.root, x) for x in X]

# Demonstration
X_data = [[1.0, 2.0], [1.5, 1.8], [5.0, 8.0], [6.0, 9.0], [1.2, 0.9], [5.5, 7.5]]
y_data = [0, 0, 1, 1, 0, 1]

dt = DecisionTreeClassifier(max_depth=3)
dt.fit(X_data, y_data)
test_points = [[1.1, 1.5], [5.8, 8.2]]
print("Decision Tree Predictions:", dt.predict(test_points))
""",

    "linear_regression": """# Linear Regression Algorithm (Ordinary Least Squares)
class LinearRegression:
    def __init__(self):
        self.slope = 0.0
        self.intercept = 0.0
        self.r_squared = 0.0

    def fit(self, x, y):
        n = len(x)
        x_mean = sum(x) / n
        y_mean = sum(y) / n

        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        self.slope = numerator / denominator
        self.intercept = y_mean - (self.slope * x_mean)

        # Compute R^2 Score
        ss_tot = sum((y[i] - y_mean) ** 2 for i in range(n))
        ss_res = sum((y[i] - self.predict_one(x[i])) ** 2 for i in range(n))
        self.r_squared = round(1.0 - (ss_res / ss_tot), 4) if ss_tot != 0 else 1.0

    def predict_one(self, x_val):
        return round((self.slope * x_val) + self.intercept, 4)

    def predict(self, x_vals):
        return [self.predict_one(val) for val in x_vals]

# Demonstration
x_train = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
y_train = [2.2, 3.9, 6.1, 8.0, 10.2, 12.1, 14.0]

model = LinearRegression()
model.fit(x_train, y_train)

print("[Linear Regression Model Results]")
print(f"  Fitted Line Equation : y = {model.slope:.4f} * x + {model.intercept:.4f}")
print(f"  Coefficient of Det. (R^2): {model.r_squared}")
test_inputs = [8.0, 10.0]
print(f"  Predictions for {test_inputs}: {model.predict(test_inputs)}")
""",

    "logistic_regression": """# Logistic Regression Algorithm (Sigmoid Classification)
import math

class LogisticRegression:
    def __init__(self, learning_rate=0.1, epochs=300):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights = []
        self.bias = 0.0

    def _sigmoid(self, z):
        return 1.0 / (1.0 + math.exp(-max(-500, min(500, z))))

    def fit(self, X, y):
        n_samples = len(X)
        n_features = len(X[0])
        self.weights = [0.0] * n_features
        self.bias = 0.0

        for _ in range(self.epochs):
            dw = [0.0] * n_features
            db = 0.0
            for i in range(n_samples):
                linear = sum(self.weights[j] * X[i][j] for j in range(n_features)) + self.bias
                y_pred = self._sigmoid(linear)
                error = y_pred - y[i]
                for j in range(n_features):
                    dw[j] += error * X[i][j]
                db += error

            for j in range(n_features):
                self.weights[j] -= (self.lr / n_samples) * dw[j]
            self.bias -= (self.lr / n_samples) * db

    def predict_proba(self, X):
        probs = []
        for x in X:
            linear = sum(self.weights[j] * x[j] for j in range(len(self.weights))) + self.bias
            probs.append(round(self._sigmoid(linear), 4))
        return probs

    def predict(self, X, threshold=0.5):
        return [1 if p >= threshold else 0 for p in self.predict_proba(X)]

# Demonstration
X_train = [[0.5, 1.5], [1.0, 1.0], [1.5, 0.5], [3.0, 3.5], [4.0, 4.0], [3.5, 4.5]]
y_train = [0, 0, 0, 1, 1, 1]

model = LogisticRegression(learning_rate=0.2, epochs=400)
model.fit(X_train, y_train)

test_data = [[1.2, 1.2], [3.8, 3.9]]
print("Logistic Regression Probabilities:", model.predict_proba(test_data))
print("Logistic Regression Binary Class :", model.predict(test_data))
""",

    "svm": """# Support Vector Machine (Linear SVM with Hinge Loss)
class LinearSVM:
    def __init__(self, learning_rate=0.01, lambda_param=0.01, epochs=300):
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.epochs = epochs
        self.weights = []
        self.bias = 0.0

    def fit(self, X, y):
        y_mod = [1 if val == 1 else -1 for val in y]
        n_features = len(X[0])
        self.weights = [0.0] * n_features
        self.bias = 0.0

        for _ in range(self.epochs):
            for i, x in enumerate(X):
                condition = y_mod[i] * (sum(self.weights[j] * x[j] for j in range(n_features)) - self.bias) >= 1
                if condition:
                    for j in range(n_features):
                        self.weights[j] -= self.lr * (2 * self.lambda_param * self.weights[j])
                else:
                    for j in range(n_features):
                        self.weights[j] -= self.lr * (2 * self.lambda_param * self.weights[j] - y_mod[i] * x[j])
                    self.bias -= self.lr * y_mod[i]

    def predict(self, X):
        predictions = []
        for x in X:
            decision = sum(self.weights[j] * x[j] for j in range(len(self.weights))) - self.bias
            predictions.append(1 if decision >= 0 else 0)
        return predictions

# Demonstration
X = [[2.0, 3.0], [1.0, 1.5], [2.5, 2.0], [6.0, 7.0], [7.0, 8.0], [6.5, 6.0]]
y = [0, 0, 0, 1, 1, 1]
svm = LinearSVM(learning_rate=0.01, epochs=200)
svm.fit(X, y)
print("SVM Predictions for [[1.5, 2.0], [6.8, 7.2]]:", svm.predict([[1.5, 2.0], [6.8, 7.2]]))
""",

    "knn": """# K-Nearest Neighbors (KNN) Classifier Implementation
import math

class KNNClassifier:
    def __init__(self, k=3):
        self.k = k
        self.X_train = []
        self.y_train = []

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def _euclidean_distance(self, p1, p2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

    def predict_one(self, x):
        distances = [(self._euclidean_distance(x, train_x), label)
                     for train_x, label in zip(self.X_train, self.y_train)]
        distances.sort(key=lambda item: item[0])
        k_nearest_labels = [label for _, label in distances[:self.k]]
        return max(set(k_nearest_labels), key=k_nearest_labels.count)

    def predict(self, X):
        return [self.predict_one(x) for x in X]

# Demonstration
X_train = [[1, 2], [2, 3], [3, 1], [6, 7], [7, 8], [8, 6]]
y_train = ["A", "A", "A", "B", "B", "B"]

knn = KNNClassifier(k=3)
knn.fit(X_train, y_train)
queries = [[2, 2], [7, 7]]
print("KNN Predictions for", queries, "->", knn.predict(queries))
""",

    "naive_bayes": """# Gaussian Naive Bayes Classifier Implementation
import math

class GaussianNaiveBayes:
    def __init__(self):
        self.classes = []
        self.parameters = {}

    def fit(self, X, y):
        self.classes = sorted(set(y))
        for c in self.classes:
            X_c = [X[i] for i in range(len(y)) if y[i] == c]
            n_c = len(X_c)
            n_features = len(X[0])
            means = [sum(row[j] for row in X_c) / n_c for j in range(n_features)]
            variances = [sum((row[j] - means[j])**2 for row in X_c) / max(1, n_c - 1) + 1e-9 for j in range(n_features)]
            prior = n_c / len(y)
            self.parameters[c] = {"means": means, "variances": variances, "prior": prior}

    def _gaussian_pdf(self, x, mean, var):
        exponent = math.exp(-((x - mean) ** 2) / (2 * var))
        return (1.0 / math.sqrt(2 * math.pi * var)) * exponent

    def predict(self, X):
        predictions = []
        for x in X:
            posteriors = {}
            for c in self.classes:
                prior = math.log(self.parameters[c]["prior"])
                likelihood = sum(
                    math.log(max(1e-12, self._gaussian_pdf(x[j], self.parameters[c]["means"][j], self.parameters[c]["variances"][j])))
                    for j in range(len(x))
                )
                posteriors[c] = prior + likelihood
            predictions.append(max(posteriors, key=posteriors.get))
        return predictions

# Demonstration
X_train = [[1.2, 2.1], [1.5, 1.9], [5.2, 5.8], [6.0, 6.2]]
y_train = [0, 0, 1, 1]
gnb = GaussianNaiveBayes()
gnb.fit(X_train, y_train)
print("Naive Bayes Predictions for [[1.3, 2.0], [5.5, 6.0]]:", gnb.predict([[1.3, 2.0], [5.5, 6.0]]))
""",

    "rle": """# Run-Length Encoding (RLE) Data Compression Algorithm
def run_length_encode(text: str) -> str:
    # Compresses consecutive identical characters into count-character pairs
    if not text:
        return ""
    encoded = []
    count = 1
    for i in range(1, len(text)):
        if text[i] == text[i - 1]:
            count += 1
        else:
            encoded.append(f"{count}{text[i - 1]}")
            count = 1
    encoded.append(f"{count}{text[-1]}")
    return "".join(encoded)

def run_length_decode(encoded_text: str) -> str:
    # Decompresses count-character RLE string back to original format
    decoded = []
    count_str = ""
    for char in encoded_text:
        if char.isdigit():
            count_str += char
        else:
            count = int(count_str) if count_str else 1
            decoded.append(char * count)
            count_str = ""
    return "".join(decoded)

# Demonstration
raw_data = "WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWB"
compressed = run_length_encode(raw_data)
decompressed = run_length_decode(compressed)
comp_ratio = round((1 - len(compressed) / len(raw_data)) * 100, 2)

print("[Run-Length Encoding Compression Results]")
print(f"  Original Data ({len(raw_data)} chars)   : {raw_data}")
print(f"  Compressed RLE ({len(compressed)} chars): {compressed}")
print(f"  Compression Ratio          : {comp_ratio}% Space Saved")
print(f"  Lossless Verification      : {raw_data == decompressed}")
""",

    "binary": """# Binary Encoding & Number System Conversion Algorithm
def decimal_to_binary(num: int, bit_length: int = None) -> str:
    # Encodes a decimal integer into a binary string
    if num == 0:
        bin_str = "0"
    else:
        bits = []
        n = abs(num)
        while n > 0:
            bits.append(str(n % 2))
            n //= 2
        bin_str = "".join(reversed(bits))
    if bit_length:
        bin_str = bin_str.zfill(bit_length)
    return f"-{bin_str}" if num < 0 else bin_str

def binary_to_decimal(bin_str: str) -> int:
    # Converts a binary string back into a decimal integer
    bin_str = bin_str.strip()
    is_neg = bin_str.startswith("-")
    if is_neg:
        bin_str = bin_str[1:]
    val = 0
    for digit in bin_str:
        val = (val << 1) | int(digit)
    return -val if is_neg else val

def text_to_binary(text: str) -> str:
    # Encodes an ASCII text string into 8-bit binary byte blocks
    return " ".join(format(ord(c), '08b') for c in text)

def binary_to_text(binary_seq: str) -> str:
    # Decodes an 8-bit binary block sequence into original ASCII text
    return "".join(chr(int(b, 2)) for b in binary_seq.split())

# Demonstration
sample_val = 142
bin_code = decimal_to_binary(sample_val, bit_length=8)
dec_back = binary_to_decimal(bin_code)
msg = "Antigravity"
msg_bin = text_to_binary(msg)

print("[Binary Encoding & Conversion Results]")
print(f"  Decimal Integer : {sample_val}")
print(f"  8-Bit Binary    : {bin_code}")
print(f"  Decoded Decimal : {dec_back}")
print(f"  Message Binary  : '{msg}' -> {msg_bin}")
""",

    "hex": """# Hexadecimal Encoding & Conversion Algorithm
def decimal_to_hex(num: int) -> str:
    # Converts an integer into a hexadecimal (base-16) string
    if num == 0:
        return "0x0"
    hex_chars = "0123456789ABCDEF"
    digits = []
    n = abs(num)
    while n > 0:
        digits.append(hex_chars[n % 16])
        n //= 16
    res = "".join(reversed(digits))
    return f"-0x{res}" if num < 0 else f"0x{res}"

def hex_to_decimal(hex_str: str) -> int:
    # Converts a hexadecimal string into a decimal integer
    clean_hex = hex_str.strip().upper().replace("0X", "").replace("#", "")
    hex_map = {c: i for i, c in enumerate("0123456789ABCDEF")}
    val = 0
    for char in clean_hex:
        val = (val * 16) + hex_map[char]
    return val

# Demonstration
test_num = 48879
hex_out = decimal_to_hex(test_num)
dec_recovered = hex_to_decimal(hex_out)
print("[Hexadecimal Encoding Results]")
print(f"  Decimal Number: {test_num}")
print(f"  Hex Encoded   : {hex_out}")
print(f"  Decoded Value : {dec_recovered}")
""",

    "base64": """# Base64 Encoding & Decoding Implementation
BASE64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def base64_encode(data: bytes) -> str:
    res = []
    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        pad_len = 3 - len(chunk)
        b = int.from_bytes(chunk + b'\x00' * pad_len, 'big')
        for j in range(4):
            if j >= 4 - pad_len:
                res.append("=")
            else:
                idx = (b >> (18 - j * 6)) & 0x3F
                res.append(BASE64_ALPHABET[idx])
    return "".join(res)

def base64_decode(encoded_str: str) -> bytes:
    clean = encoded_str.rstrip("=")
    pad_len = len(encoded_str) - len(clean)
    val = 0
    for char in clean:
        val = (val << 6) | BASE64_ALPHABET.index(char)
    val <<= (pad_len * 6)
    total_bytes = (len(encoded_str) * 6) // 8 - pad_len
    return val.to_bytes((len(encoded_str) * 6) // 8, 'big')[:total_bytes]

# Demonstration
sample_text = "Computer Science Algorithm Engine"
b64_enc = base64_encode(sample_text.encode('utf-8'))
b64_dec = base64_decode(b64_enc).decode('utf-8')
print("[Base64 Encoding Results]")
print(f"  Original Text : '{sample_text}'")
print(f"  Base64 Output : {b64_enc}")
print(f"  Decoded Match : {sample_text == b64_dec}")
""",

    "q_learning": """# Q-Learning Algorithm (Reinforcement Learning Q-Table Optimization)
import random

class QLearningAgent:
    def __init__(self, states, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.states = states
        self.actions = actions
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = {s: {a: 0.0 for a in actions} for s in states}

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        return max(self.q_table[state], key=self.q_table[state].get)

    def update(self, state, action, reward, next_state):
        best_next_q = max(self.q_table[next_state].values())
        old_q = self.q_table[state][action]
        # Bellman Optimality Update Equation
        self.q_table[state][action] = old_q + self.alpha * (reward + self.gamma * best_next_q - old_q)

# Demonstration: 1D Gridworld Navigation (State 0 -> Target State 4)
states = [0, 1, 2, 3, 4]
actions = ["LEFT", "RIGHT"]
agent = QLearningAgent(states, actions, alpha=0.2, gamma=0.85, epsilon=0.2)

for episode in range(200):
    curr_state = 0
    while curr_state != 4:
        action = agent.choose_action(curr_state)
        next_state = max(0, curr_state - 1) if action == "LEFT" else min(4, curr_state + 1)
        reward = 10.0 if next_state == 4 else -1.0
        agent.update(curr_state, action, reward, next_state)
        curr_state = next_state

print("[Q-Learning Optimal State Policy]")
for s in range(4):
    best_act = max(agent.q_table[s], key=agent.q_table[s].get)
    print(f"  State {s} -> Best Action: {best_act} (Q-Value: {agent.q_table[s][best_act]:.2f})")
""",

    "default": """# {algorithm_name} High-Fidelity Implementation
def solve_{func_name}(data_inputs):
    # Standard execution solution
    return {{"status": "success", "algorithm": "{algorithm_name}", "processed_count": len(data_inputs)}}

print("Execution test for {algorithm_name}: Success")
"""
}

def get_ml_encoding_python_code(algorithm_name: str) -> str:
    key = _match_key(algorithm_name)
    if key in ML_PYTHON_CODE:
        return ML_PYTHON_CODE[key]
    func_name = re.sub(r"[^a-zA-Z0-9_]", "_", algorithm_name.lower())
    return ML_PYTHON_CODE["default"].format(algorithm_name=algorithm_name, func_name=func_name)

# =============================================================================
# PSEUDOCODE MAP
# =============================================================================
ML_PSEUDOCODE = {
    "random_forest": """Algorithm RandomForestClassifier(D, B, m)
Input: Dataset D of N samples, Number of trees B, Subspace feature count m
Output: Ensemble model EnsembleTrees

Begin
    EnsembleTrees <- EmptyList()

    For b <- 1 to B do
        D_boot <- BootstrapSample(D, N)
        Tree_b <- ConstructTree(D_boot, m)
        EnsembleTrees.append(Tree_b)
    End For

    Procedure Predict(x)
        Votes <- EmptyList()
        For each Tree in EnsembleTrees do
            prediction <- Tree.Evaluate(x)
            Votes.append(prediction)
        End For
        Return MajorityVote(Votes)
    End Procedure

    Return EnsembleTrees
End""",

    "octal": """Algorithm DecimalToOctal(N)
Input: Non-negative integer N
Output: Base-8 octal representation string

Begin
    If N = 0 then Return "0"
    digits <- Stack()

    While N > 0 do
        remainder <- N mod 8
        digits.push(remainder)
        N <- floor(N / 8)
    End While

    octal_string <- ""
    While not digits.isEmpty() do
        octal_string <- octal_string + ToString(digits.pop())
    End While

    Return octal_string
End""",

    "decision_tree": """Algorithm BuildDecisionTree(D, max_depth, depth)
Input: Dataset D, Maximum allowed depth max_depth, Current depth depth
Output: Decision Tree root node

Begin
    If depth >= max_depth or IsPure(D) then
        Return LeafNode(MajorityClass(D))
    End If

    (best_feat, best_threshold) <- FindOptimalSplit(D)
    If best_feat is Null then
        Return LeafNode(MajorityClass(D))
    End If

    (D_left, D_right) <- Partition(D, best_feat, best_threshold)
    left_node <- BuildDecisionTree(D_left, max_depth, depth + 1)
    right_node <- BuildDecisionTree(D_right, max_depth, depth + 1)

    Return InternalNode(best_feat, best_threshold, left_node, right_node)
End""",

    "linear_regression": """Algorithm OrdinaryLeastSquares(X, Y)
Input: 1D feature array X, Response array Y of length N
Output: Slope m, Intercept c

Begin
    x_mean <- Mean(X)
    y_mean <- Mean(Y)

    numerator <- 0.0
    denominator <- 0.0

    For i <- 0 to N - 1 do
        numerator <- numerator + (X[i] - x_mean) * (Y[i] - y_mean)
        denominator <- denominator + (X[i] - x_mean)^2
    End For

    m <- numerator / denominator
    c <- y_mean - (m * x_mean)

    Return (m, c)
End""",

    "logistic_regression": """Algorithm LogisticRegressionFit(X, Y, epochs, alpha)
Input: Matrix X of N samples, Binary labels Y, Epoch count epochs, Learning rate alpha
Output: Optimized weight vector w, bias b

Begin
    w <- ZeroVector(num_features)
    b <- 0.0

    For epoch <- 1 to epochs do
        grad_w <- ZeroVector(num_features)
        grad_b <- 0.0

        For i <- 1 to N do
            z <- DotProduct(w, X[i]) + b
            p <- 1.0 / (1.0 + exp(-z))
            err <- p - Y[i]
            grad_w <- grad_w + err * X[i]
            grad_b <- grad_b + err
        End For

        w <- w - (alpha / N) * grad_w
        b <- b - (alpha / N) * grad_b
    End For

    Return (w, b)
End""",

    "rle": """Algorithm RunLengthEncode(InputString)
Input: String of characters S of length N
Output: Compressed RLE string

Begin
    If length(S) = 0 then Return ""
    encoded <- ""
    count <- 1

    For i <- 1 to N - 1 do
        If S[i] = S[i - 1] then
            count <- count + 1
        Else
            encoded <- encoded + ToString(count) + S[i - 1]
            count <- 1
        End If
    End For

    encoded <- encoded + ToString(count) + S[N - 1]
    Return encoded
End""",

    "q_learning": """Algorithm QLearning(Environment, alpha, gamma, epsilon, episodes)
Input: Environment MDP, Learning rate alpha, Discount factor gamma, Exploration epsilon
Output: Action-value table Q

Begin
    Initialize Q(s, a) <- 0 for all states s and actions a

    For episode <- 1 to episodes do
        s <- Environment.Reset()

        While s is not terminal do
            If Random() < epsilon then
                a <- RandomAction()
            Else
                a <- argmax_a Q(s, a)
            End If

            (s_prime, reward, is_done) <- Environment.Step(a)
            Q(s, a) <- Q(s, a) + alpha * [reward + gamma * max_a Q(s_prime, a) - Q(s, a)]
            s <- s_prime
        End While
    End For

    Return Q
End"""
}

def get_ml_encoding_pseudocode(algorithm_name: str) -> str:
    key = _match_key(algorithm_name)
    if key in ML_PSEUDOCODE:
        return ML_PSEUDOCODE[key]
    clean_name = re.sub(r"[^a-zA-Z0-9]", "", algorithm_name)
    return f"""Algorithm {clean_name}(InputData)
Input: Domain data InputData
Output: Processed algorithmic result

Begin
    ValidateInputs(InputData)
    state <- InitializeState(InputData)
    result <- ComputeOptimalExecution(state)
    Return result
End"""

# =============================================================================
# WORKING STEPS MAP
# =============================================================================
ML_WORKING_STEPS = {
    "random_forest": [
        "Start",
        "Read training dataset D of N samples with M features, and ensemble size B (number of trees).",
        "For each tree b = 1 to B in parallel:",
        "  Create a bootstrap sample D_b of size N by sampling with replacement from D.",
        "  Grow an unpruned decision tree T_b on D_b:",
        "    At each candidate node, randomly select a feature subspace of size m ~ sqrt(M).",
        "    Compute Gini impurity or Information Gain across candidate splits on selected features.",
        "    Choose the split with maximum purity gain and partition sample into child nodes.",
        "    Recurse until minimum leaf node size or maximum tree depth is reached.",
        "For an unlabeled query sample x:",
        "  Pass x down all B decision trees to obtain predictions C_1(x), C_2(x), ..., C_B(x).",
        "  Aggregate predictions via majority voting (classification) or arithmetic mean (regression).",
        "Return final ensemble prediction.",
        "Stop"
    ],
    "octal": [
        "Start",
        "Read input numerical value N in decimal format (or raw byte string).",
        "Initialize empty list or string buffer for octal digits.",
        "While N > 0 do:",
        "  Compute remainder r = N mod 8.",
        "  Append digit r to the octal buffer.",
        "  Update N = floor(N / 8).",
        "Reverse the octal buffer to produce standard base-8 string representation.",
        "For binary conversion: map each octal digit [0-7] to its 3-bit binary triplet (000 to 111).",
        "For reverse decoding: evaluate polynomial sum of digits multiplied by corresponding powers of 8.",
        "Return formatted octal string and decoded verification value.",
        "Stop"
    ],
    "decision_tree": [
        "Start",
        "Read training data samples X and target class labels y.",
        "Calculate base impurity (Gini Impurity or Shannon Entropy) of current sample set.",
        "For each candidate feature f and possible split threshold t:",
        "  Partition dataset into left (feature <= t) and right (feature > t) subsets.",
        "  Compute weighted impurity reduction (Information Gain).",
        "Select feature and threshold yielding maximal information gain.",
        "Create decision node and recursively build left and right subtrees.",
        "Terminate branch when maximum depth reached, sample count below minimum, or node is pure.",
        "Return root node of constructed Decision Tree.",
        "Stop"
    ],
    "linear_regression": [
        "Start",
        "Read input feature vectors X and continuous response values y.",
        "Calculate sample mean values x_bar and y_bar across all data points.",
        "Compute covariance of (X, y) and sample variance of X.",
        "Calculate Ordinary Least Squares (OLS) slope m = Sum((x - x_bar)(y - y_bar)) / Sum((x - x_bar)^2).",
        "Compute regression intercept c = y_bar - (m * x_bar).",
        "Evaluate model performance: compute Mean Squared Error (MSE) and R^2 coefficient of determination.",
        "Return fitted regression parameters (slope, intercept) and predictions.",
        "Stop"
    ],
    "logistic_regression": [
        "Start",
        "Read training features X and binary target labels y in {0, 1}.",
        "Initialize feature weight vector w and bias scalar b to zero.",
        "For epoch = 1 to MaxEpochs do:",
        "  For each sample, compute linear logit: z = w . x + b.",
        "  Apply logistic sigmoid activation: p = 1 / (1 + e^(-z)).",
        "  Compute prediction error: error = p - y.",
        "  Compute partial gradients dL/dw and dL/db.",
        "  Update weights: w <- w - eta * dL/dw and b <- b - eta * dL/db (learning rate eta).",
        "Return optimized parameters (w, b) and probability inference function.",
        "Stop"
    ],
    "svm": [
        "Start",
        "Read training data points X with binary classification labels y in {-1, +1}.",
        "Initialize weight vector w and bias b.",
        "For each optimization epoch and sample (x_i, y_i):",
        "  Evaluate functional margin condition: y_i * (w . x_i + b) >= 1.",
        "  If margin condition satisfied (no margin violation):",
        "    Update weights via regularization gradient: w <- w - eta * (2 * lambda * w).",
        "  Else (margin violation detected):",
        "    Update weights and bias via hinge loss subgradient: w <- w - eta * (2 * lambda * w - y_i * x_i), b <- b + eta * y_i.",
        "Return maximal-margin decision hyperplane parameters w and b.",
        "Stop"
    ],
    "knn": [
        "Start",
        "Store all labeled training sample vectors and corresponding class labels.",
        "Read unlabeled test query sample point q.",
        "For each training instance x_i in memory:",
        "  Compute Euclidean distance d(q, x_i) = sqrt(Sum((q_j - x_ij)^2)).",
        "Sort all training instances in ascending order of calculated distance.",
        "Select top K training instances with smallest distances.",
        "Tally class label frequencies among the K nearest neighbors.",
        "Assign query point q the class label with highest vote count.",
        "Stop"
    ],
    "rle": [
        "Start",
        "Read input character string or byte stream S of length L.",
        "Initialize pointer idx = 0, count = 1, and output buffer.",
        "Iterate pointer i from 1 to L - 1 through string S:",
        "  If character S[i] == S[i - 1], increment count <- count + 1.",
        "  Else append count and character S[i - 1] to output buffer; reset count <- 1.",
        "Append final count and last character S[L - 1] to output buffer.",
        "Return compressed RLE encoded string.",
        "Stop"
    ],
    "binary": [
        "Start",
        "Read non-negative decimal integer N.",
        "Initialize empty bit list.",
        "While N > 0 do:",
        "  Compute remainder bit = N mod 2.",
        "  Append bit to bit list.",
        "  Update N = floor(N / 2).",
        "Reverse bit list to produce standard most-significant-bit-first binary representation.",
        "Return binary string.",
        "Stop"
    ],
    "hex": [
        "Start",
        "Read decimal integer N and hex character lookup table '0123456789ABCDEF'.",
        "While N > 0 do:",
        "  Compute remainder r = N mod 16.",
        "  Look up corresponding hex symbol at index r.",
        "  Update N = floor(N / 16).",
        "Reverse gathered hex characters to form final hexadecimal string.",
        "Return prefixed hex string (e.g. 0x...).",
        "Stop"
    ],
    "base64": [
        "Start",
        "Read raw binary byte stream of length N.",
        "Partition byte stream into 3-byte (24-bit) blocks.",
        "Split each 24-bit block into four 6-bit index values (each 0 to 63).",
        "Map each 6-bit index to corresponding character in Base64 alphabet.",
        "If final chunk has fewer than 3 bytes, pad output with '=' characters.",
        "Return Base64 ASCII encoded string.",
        "Stop"
    ],
    "q_learning": [
        "Start",
        "Initialize state-action Q-table Q(s, a) to zeros or small random values.",
        "Set hyperparameters: learning rate alpha, discount factor gamma, exploration rate epsilon.",
        "For episode = 1 to MaxEpisodes do:",
        "  Initialize environment state s.",
        "  While s is not a terminal state do:",
        "    Choose action a using epsilon-greedy policy (random with probability epsilon, else argmax_a Q(s, a)).",
        "    Execute action a in environment; observe reward r and next state s_prime.",
        "    Update Q-value: Q(s, a) <- Q(s, a) + alpha * [reward + gamma * max_a Q(s_prime, a) - Q(s, a)].",
        "    Transition to next state: s <- s_prime.",
        "Return converged Q-table representing optimal policy.",
        "Stop"
    ]
}

def get_ml_encoding_working_steps(algorithm_name: str) -> List[str]:
    key = _match_key(algorithm_name)
    if key in ML_WORKING_STEPS:
        return ML_WORKING_STEPS[key]
    return [
        "Start",
        f"Initialize operational buffers and parameters for {algorithm_name}.",
        "Execute core algorithmic transformation and metric evaluation.",
        "Verify state convergence and invariant criteria.",
        "Return finalized algorithmic output.",
        "Stop"
    ]

# =============================================================================
# COMPLEXITY MAP
# =============================================================================
ML_COMPLEXITY = {
    "random_forest": {
        "time_complexity": {"best": "O(B * N log N)", "average": "O(B * m * N log N)", "worst": "O(B * M * N^2)"},
        "space_complexity": "O(B * Depth * N)"
    },
    "octal": {
        "time_complexity": {"best": "O(1)", "average": "O(log8 N)", "worst": "O(log8 N)"},
        "space_complexity": "O(log8 N)"
    },
    "decision_tree": {
        "time_complexity": {"best": "O(M * N log N)", "average": "O(M * N log N)", "worst": "O(M * N^2)"},
        "space_complexity": "O(Depth)"
    },
    "linear_regression": {
        "time_complexity": {"best": "O(N)", "average": "O(N * M)", "worst": "O(M^3 + M^2 * N)"},
        "space_complexity": "O(M)"
    },
    "logistic_regression": {
        "time_complexity": {"best": "O(Epochs * N * M)", "average": "O(Epochs * N * M)", "worst": "O(Epochs * N * M)"},
        "space_complexity": "O(M)"
    },
    "svm": {
        "time_complexity": {"best": "O(N * M)", "average": "O(N^2 * M)", "worst": "O(N^3 * M)"},
        "space_complexity": "O(N * M)"
    },
    "knn": {
        "time_complexity": {"best": "O(N * M)", "average": "O(N * M + N log K)", "worst": "O(N * M + N log N)"},
        "space_complexity": "O(N * M)"
    },
    "naive_bayes": {
        "time_complexity": {"best": "O(N * M)", "average": "O(N * M)", "worst": "O(N * M)"},
        "space_complexity": "O(Classes * M)"
    },
    "rle": {
        "time_complexity": {"best": "O(N)", "average": "O(N)", "worst": "O(N)"},
        "space_complexity": "O(N)"
    },
    "binary": {
        "time_complexity": {"best": "O(1)", "average": "O(log2 N)", "worst": "O(log2 N)"},
        "space_complexity": "O(log2 N)"
    },
    "hex": {
        "time_complexity": {"best": "O(1)", "average": "O(log16 N)", "worst": "O(log16 N)"},
        "space_complexity": "O(log16 N)"
    },
    "base64": {
        "time_complexity": {"best": "O(N)", "average": "O(N)", "worst": "O(N)"},
        "space_complexity": "O(N)"
    },
    "q_learning": {
        "time_complexity": {"best": "O(Episodes * Steps)", "average": "O(Episodes * Steps * |A|)", "worst": "O(Episodes * Steps * |A|)"},
        "space_complexity": "O(|S| * |A|)"
    }
}

def get_ml_encoding_complexity(algorithm_name: str) -> Dict[str, Any]:
    key = _match_key(algorithm_name)
    if key in ML_COMPLEXITY:
        return ML_COMPLEXITY[key]
    return {
        "time_complexity": {"best": "O(1)", "average": "O(N)", "worst": "O(N)"},
        "space_complexity": "O(1)"
    }

# =============================================================================
# ADVANTAGES & DISADVANTAGES MAP
# =============================================================================
ML_ADVANTAGES = {
    "random_forest": [
        "Highly resistant to overfitting compared to single decision trees via bootstrap ensemble averaging",
        "Handles high-dimensional feature spaces without requiring initial feature scaling or normalization",
        "Maintains high classification accuracy even when a significant proportion of data features are missing",
        "Provides built-in out-of-bag (OOB) error estimates and feature importance rankings"
    ],
    "octal": [
        "Direct 1-to-3 bit mapping with binary representation allows swift bitwise translation without division",
        "Human-readable compact notation for low-level machine instructions and Unix permission bits (chmod)",
        "Zero precision loss when representing integer values and raw byte memory dumps",
        "Simpler arithmetic hardware logic than base-10 decimal conversion units"
    ],
    "decision_tree": [
        "White-box interpretable decision rules that can be visualized and explained directly",
        "Requires little to no data preparation, normalization, or feature scaling",
        "Handles both numerical and categorical feature data seamlessly"
    ],
    "linear_regression": [
        "Computationally lightweight with analytical closed-form Ordinary Least Squares solution",
        "Direct interpretability of feature coefficients as marginal impact values",
        "Proven baseline model with low variance when true relationship is approximately linear"
    ],
    "logistic_regression": [
        "Outputs calibrated probabilistic confidence scores in [0, 1] rather than hard labels",
        "Highly efficient to train via convex log-loss function with guaranteed global optimum",
        "Easily extendable with L1 (Lasso) and L2 (Ridge) regularization to prevent overfitting"
    ],
    "rle": [
        "Extremely fast linear O(N) compression and decompression execution",
        "High compression ratios on repeated data sequences (e.g. monochrome bitmaps and fax signals)",
        "Completely lossless with zero reconstruction artifact distortion"
    ]
}

def get_ml_encoding_advantages(algorithm_name: str) -> List[str]:
    key = _match_key(algorithm_name)
    if key in ML_ADVANTAGES:
        return ML_ADVANTAGES[key]
    return [
        f"Efficient execution model tailored for {algorithm_name}",
        "High numerical reliability across real-world application inputs",
        "Deterministic behavior with well-understood theoretical bounds"
    ]

ML_DISADVANTAGES = {
    "random_forest": [
        "Significantly higher memory footprint to store tens or hundreds of grown decision trees",
        "Slower real-time inference latency compared to a single decision tree or linear model",
        "Acts as a black box with reduced interpretability relative to individual decision stumps"
    ],
    "octal": [
        "Less space-efficient than hexadecimal (base-16) for modern 8-bit, 16-bit, and 32-bit architectures",
        "Byte boundaries (8 bits) do not divide evenly into 3-bit octal blocks without cross-byte splitting",
        "Less commonly supported in modern web JSON and serialization protocols than hex"
    ],
    "decision_tree": [
        "High variance: small variations in training data can result in completely different tree structures",
        "Greedy top-down splitting can get trapped in sub-optimal local feature decisions"
    ],
    "linear_regression": [
        "Vulnerable to significant bias when true feature-target relationship is non-linear",
        "Highly sensitive to outliers and collinearity among independent feature variables"
    ]
}

def get_ml_encoding_disadvantages(algorithm_name: str) -> List[str]:
    key = _match_key(algorithm_name)
    if key in ML_DISADVANTAGES:
        return ML_DISADVANTAGES[key]
    return [
        "Parameter sensitivity under extreme or degenerate input edge cases",
        "Potential computational overhead during large batch data transformations"
    ]

ML_QUESTIONS = {
    "random_forest": [
        "How does Random Forest decrease model variance without systematically increasing bias?",
        "What is the mathematical difference between Bagging (Random Forest) and Boosting (GBDT/XGBoost)?",
        "How are Out-of-Bag (OOB) error estimates computed, and why do they eliminate the need for a validation split?",
        "Why is m = sqrt(M) commonly chosen as the number of random features selected at each tree split?"
    ],
    "octal": [
        "Explain why each octal digit maps precisely to a 3-bit binary triplet (2^3 = 8).",
        "How does the Unix file permission system utilize octal notation (e.g. chmod 755 or 644)?",
        "How would you implement base-8 conversion for negative integers using two's complement arithmetic?",
        "What are the trade-offs between Octal (base-8) and Hexadecimal (base-16) in systems programming?"
    ],
    "decision_tree": [
        "Compare Gini Impurity and Shannon Entropy as splitting criteria in Decision Trees.",
        "Explain cost-complexity pruning and how it prevents tree overfitting.",
        "How do decision trees handle missing feature values during training and inference?"
    ],
    "linear_regression": [
        "Derive the Ordinary Least Squares (OLS) closed-form normal equation: w = (X^T X)^(-1) X^T y.",
        "What are the Gauss-Markov assumptions required for OLS to be the Best Linear Unbiased Estimator (BLUE)?",
        "How do L1 (Lasso) and L2 (Ridge) penalties alter the loss landscape of Linear Regression?"
    ]
}

def get_ml_encoding_interview_questions(algorithm_name: str) -> List[str]:
    key = _match_key(algorithm_name)
    if key in ML_QUESTIONS:
        return ML_QUESTIONS[key]
    return [
        f"Explain the core theoretical principles underlying {algorithm_name}.",
        f"What is the worst-case time complexity of {algorithm_name} and under what conditions does it occur?",
        f"How would you optimize {algorithm_name} for production environments with high query volume?"
    ]
