# ExamScan
A Python 3 script to evaluate single and multiple choice exam sheets.

## Example

Input image:

![Example Image](/example/test.png)

Processed image:

![Processed Image](/example/test_eval.png)

## Usage

`main.py (-u URL | -f FILE) -n NUM [-h] [-i IOUT] [-d DOUT] [-c COMP] [-p]`

#### Flags:
##### Required, but mutually exclusive flags:
| Short | Long | Description |
| -- | -- | -- |
| -u URL | --url URL | URL to the image or pdf to be evaluated |
| -f FILE | --file FILE | path to the image or pdf to be evaluated |

##### Required flags:
| Short | Long | Description |
| -- | -- | -- |
| -n NUM | --num NUM | number of answers per question |

##### Optional flags:
| Short | Long | Description |
| -- | -- | -- |
|-h | --help | shows help message and exits |
| -i IOUT | --iout IOUT | path for the output picture to be stored. |
| -d DOUT | --dout DOUT | path for the output data to be stored. |
| -c COMP | --compare COMP | compares the calculated result to a given result |
| -p | --plot | plots every single step |

## Requirements:
| Module | Pip | Git |
| -- | -- | -- |
| OpenCV | [opencv-python](https://pypi.org/project/opencv-python/) | [skvark/opencv-python](https://github.com/skvark/opencv-python) |
| NumPy | [numpy](https://pypi.org/project/numpy/) | [numpy/numpy](https://github.com/numpy/numpy) |
| Matplotlib | [matplotlib](https://pypi.org/project/matplotlib/) | [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) |
| imutils | [imutils](https://pypi.org/project/imutils/) | [jrosebr1/imutils](https://github.com/jrosebr1/imutils) |
| python-magic | [python-magic](https://pypi.org/project/python-magic/) | [ahupp/python-magic](https://github.com/ahupp/python-magic) |
| pdf2image | [pdf2image](https://pypi.org/project/pdf2image/) | [Belval/pdf2image](https://github.com/Belval/pdf2image) | 