int is_alpha(char c) {
        return ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'));
    }

    int is_upper(char c) {
        return (c >= 'A' && c <= 'Z');
    }

// Encryption key
__constant char encryptKey[26] = "CISQVNFOWAXMTGUHPBKLREYDZJ";

// Decryption key
__constant char decryptKey[26] = "jraxvgnpbzstlfhqducmoeikwy";

    __kernel void encrypt_Decrypt(__global char* input, __global unsigned char *output, int n) {
        int i = get_global_id(0);
        char c = input[i];
        if (is_alpha(c)) {
            char a = is_upper(c) ? 'A' : 'a';
            output[i] = (c - a + n + 26) % 26 + a;
        } else {
            output[i] = c;
        }
    }

    // Encrypt function
__kernel void encrypt(__global const char* input, __global char* output)
{
    int index = get_global_id(0);
    char c = input[index];
    if (c >= 'a' && c <= 'z')
    {
        int keyIndex = c - 'a';
        output[index] = encryptKey[keyIndex];
    }
    else if (c >= 'A' && c <= 'Z')
    {
        int keyIndex = c - 'A';
        output[index] = encryptKey[keyIndex];
    }
    else
    {
        output[index] = c;
    }
}

// Decrypt function
__kernel void decrypt(__global const char* input, __global char* output)
{
    int index = get_global_id(0);
    char c = input[index];
    if (c >= 'a' && c <= 'z')
    {
        int keyIndex = c - 'a';
        output[index] = decryptKey[keyIndex];
    }
    else if (c >= 'A' && c <= 'Z')
    {
        int keyIndex = c - 'A';
        output[index] = decryptKey[keyIndex];
    }
    else
    {
        output[index] = c;
    }
}