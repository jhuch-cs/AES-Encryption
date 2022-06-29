from byte import Byte
from word import Word
from util import *

class Aes:
    num_rounds = {128: 10, 192: 12, 256: 14}

    # key should be an array of Bytes with bit length `num_bits`
    def __init__(self, num_bits = 128, key = []):
        self.num_bits = num_bits
        self.key = key
        self.key_expansion()

    def apply_s_box(self, byte):
        return Byte(s_box[byte.get_nibble(0)][byte.get_nibble(1)])

    def apply_inv_s_box(self, byte):
        return Byte(inv_s_box[byte.get_nibble(0)][byte.get_nibble(1)])

    def sub_word(self, word):
        return Word([self.apply_s_box(word[i]) for i in range(4)])

    def rotate(self, arr, by = 0):
        return arr[by:] + arr[:by]

    def rot_word(self, word):
        return Word(self.rotate(word, by = 1))

    def key_expansion(self):
        n_k = self.num_bits // 32
        n_r = Aes.num_rounds[self.num_bits]
        w = []

        for i in range(n_k):
            w.append(Word([self.key[4 * i], self.key[4 * i + 1], self.key[4 * i + 2], self.key[4 * i + 3]]))
        
        for i in range(n_k, 4 * (n_r + 1)):
            temp = w[i - 1]
            if (i % n_k == 0):
                temp = self.sub_word(self.rot_word(temp)) ^ Word.from_4bytes(r_con[i // n_k])
            elif (n_k > 6 and i % n_k == 4):
                temp = self.sub_word(temp)
            w.append(w[i - n_k] ^ temp)

        self.key_schedule = w

    def sub_bytes(self, state, round):
        new_state = [[self.apply_s_box(state[i][j]) for j in range(4)] for i in range(4)]
        eprint(f"round[{round}].s_box\t\t" + to_hex_from_bytes(ungroup_column_major(new_state)))
        return new_state

    def inv_sub_bytes(self, state, round):
        new_state = [[self.apply_inv_s_box(state[i][j]) for j in range(4)] for i in range(4)]
        eprint(f"round[{round}].i_box\t\t" + to_hex_from_bytes(ungroup_column_major(new_state)))
        return new_state
                
    def shift_rows(self, state, round):
        new_state = [self.rotate(state[i], i) for i in range(4)]
        eprint(f"round[{round}].s_row\t\t" + to_hex_from_bytes(ungroup_column_major(new_state)))
        return new_state

    def inv_shift_rows(self, state, round):
        new_state = [self.rotate(state[i], -1 * i) for i in range(4)]
        eprint(f"round[{round}].i_row\t\t" + to_hex_from_bytes(ungroup_column_major(new_state)))
        return new_state

    def mix_columns(self, state, round):
        new_state = [[0 for _ in range(4)] for _ in range(4)]
        two   = Byte(0x02)
        three = Byte(0x03)
        for c in range(4):
            new_state[0][c] = (two * state[0][c]) + (three * state[1][c]) + state[2][c] + state[3][c]
            new_state[1][c] = state[0][c] + (two * state[1][c]) + (three * state[2][c]) + state[3][c]
            new_state[2][c] = state[0][c] + state[1][c] + (two * state[2][c]) + (three * state[3][c])
            new_state[3][c] = (three * state[0][c]) + state[1][c] + state[2][c] + (two * state[3][c])
        eprint(f"round[{round}].m_col\t\t" + to_hex_from_bytes(ungroup_column_major(new_state)))
        return new_state

    def inv_mix_columns(self, state, round):
        new_state = [[0 for _ in range(4)] for _ in range(4)]
        e    = Byte(0x0e)
        b    = Byte(0x0b)
        d    = Byte(0x0d)
        nine = Byte(0x09)
        for c in range(4):
            new_state[0][c] = e * state[0][c] + b * state[1][c] + d * state[2][c] + nine * state[3][c]
            new_state[1][c] = nine * state[0][c] + e * state[1][c] + b * state[2][c] + d * state[3][c]
            new_state[2][c] = d * state[0][c] + nine * state[1][c] + e * state[2][c] + b * state[3][c]
            new_state[3][c] = b * state[0][c] + d * state[1][c] + nine * state[2][c] + e * state[3][c]
        return new_state
    
    def add_round_key(self, state, round = 0, is_inv = False):
        eprint(f"round[{round}].k_sch\t\t" + to_hex_from_words(self.key_schedule[round * 4:round * 4 + 4]))
        for c in range(4):
            column = Word([state[0][c], state[1][c], state[2][c], state[3][c]]) ^ self.key_schedule[round * 4 + c]
            state[0][c] = column.bytes[0]
            state[1][c] = column.bytes[1]
            state[2][c] = column.bytes[2]
            state[3][c] = column.bytes[3]
        if (is_inv):
            eprint(f"round[{round}].k_add\t\t" + to_hex_from_bytes(ungroup_column_major(state)))
        return state

    # input: flat list of 16 bytes
    def cipher(self, input):
        n_r = Aes.num_rounds[self.num_bits]
        eprint("round[0].input\t\t" + to_hex_from_bytes(input))

        state = group_column_major(input)

        state = self.add_round_key(state, 0)
        for round in range(1, n_r):
            eprint(f"round[{round}].start\t\t" + to_hex_from_bytes(ungroup_column_major(state)))
            state = self.sub_bytes(state, round)
            state = self.shift_rows(state, round)
            state = self.mix_columns(state, round)
            state = self.add_round_key(state, round)
        
        eprint(f"round[{n_r}].start\t\t" + to_hex_from_bytes(ungroup_column_major(state)))
        state = self.sub_bytes(state, n_r)
        state = self.shift_rows(state, n_r)
        state = self.add_round_key(state, n_r)

        output = ungroup_column_major(state)
        eprint(f"round[{n_r}].output\t" + to_hex_from_bytes(output))
        return output

    # input: flat list of 16 bytes
    def decipher(self, input):
        n_r = Aes.num_rounds[self.num_bits]
        eprint(f"round[{n_r}].input\t\t" + to_hex_from_bytes(input))

        state = group_column_major(input)

        state = self.add_round_key(state, n_r, True)
        for round in range(n_r - 1, 0, -1):
            eprint(f"round[{round}].start\t\t" + to_hex_from_bytes(ungroup_column_major(state)))
            state = self.inv_shift_rows(state, round)
            state = self.inv_sub_bytes(state, round)
            state = self.add_round_key(state, round, True)
            state = self.inv_mix_columns(state, round)
        
        eprint("round[0].start\t\t" + to_hex_from_bytes(ungroup_column_major(state)))
        state = self.inv_shift_rows(state, 0)
        state = self.inv_sub_bytes(state, 0)
        state = self.add_round_key(state, 0, True)

        output = ungroup_column_major(state)
        eprint("round[0].ioutput\t" + to_hex_from_bytes(output))
        return output