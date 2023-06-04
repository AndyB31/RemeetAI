from ..utils import debug


def combine_words(splitted_input, input, length):
    combined_inputs = []
    if len(splitted_input) > 1:
        for i in range(len(input) - 1):
            combined_inputs.append(input[i] + " " + last_word_of(splitted_input[i + 1], length)) #add the last word of the right-neighbour (overlapping) sequence (before it has expanded), which is the next word in the original sentence
    return combined_inputs, length + 1

def remove_duplicates_step(input, length):
    bool_broke=False #this means we didn't find any duplicates here
    for i in range(len(input) - length):
        if input[i] == input[i + length]: #found a duplicate piece of sentence!
            for j in range(0, length): #remove the overlapping sequences in reverse order
                del input[i + length - j]
            bool_broke = True
            break #break the for loop as the loop length does not matches the length of splitted_input anymore as we removed elements
    if bool_broke:
        return remove_duplicates_step(input, length) #if we found a duplicate, look for another duplicate of the same length
    return input

def last_word_of(input, length):
    splitted = input.split(" ")
    if len(splitted) == 0:
        return input
    else:
        return splitted[length - 1]

#make a list of strings which represent every sequence of word_length adjacent words

def remove_duplicates(input: str) -> str:
  splitted_input = input.split(" ")
  word_length = 1
  splitted_input, word_length = combine_words(splitted_input, splitted_input, word_length)

  intermediate_output = False

  while len(splitted_input) > 1:
      splitted_input = remove_duplicates_step(splitted_input, word_length) #look whether two sequences of length n (with distance n apart) are equal. If so, remove the n overlapping sequences
      splitted_input, word_length = combine_words(splitted_input, splitted_input, word_length) #make even bigger sequences
      if intermediate_output:
          debug.print_debug(splitted_input)
          debug.print_debug(word_length)
  output = splitted_input[0] #In the end you have a list of length 1, with all possible lengths of repetitive words removed
  return output