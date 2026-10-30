from flask import Flask, request, jsonify
import math
import os

app = Flask(__name__)
# Limit incoming requests to 1 MB
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

@app.route("/", methods=["GET"])
def home():
    return "Minitab Service is Running!"

#Health check endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

#Check if the input is a non empty array of ints
def validate_input(nums):
    #Check if input is a list/array
    if not isinstance(nums, list):
        return "Must be an array of numbers"

    #Check if array is empty
    if len(nums) == 0:
        return "Must contain at least one number"

    #Check if the array contains only ints or floats 
    if any(isinstance(n, bool) or not isinstance(n, (int, float)) for n in nums):
        return "All values must be numbers"

    #Check for NaN and infinity
    if any(isinstance(n, float) and not math.isfinite(n) for n in nums):
        return "All values must be finite numbers"

    return None

#Return the mean of an array of nums
@app.route("/mean", methods=["POST"])
def calculate_mean():
    nums = request.get_json(silent=True)

    error = validate_input(nums)
    if error:
        return jsonify({"error": error}), 400

    mean = sum(nums) / len(nums)

    #f converts the int to a strinng so its possible to remove trailing 0s with :g
    return f"{round(mean, 3):g}"

#Return the population standard deviation of an array of nums
@app.route("/stddev", methods=["POST"])
def calculate_stddev():
    nums = request.get_json(silent=True)

    error = validate_input(nums)
    if error:
        return jsonify({"error": error}), 400

    mean = sum(nums) / len(nums)

    variance = sum((n - mean) ** 2 for n in nums) / len(nums)
    stddev = math.sqrt(variance)

    return f"{round(stddev, 3):g}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
