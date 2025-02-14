import argparse
import hashlib
import binascii
import json


class MerkleVerification:
    def __init__(self):
        self.parser = self._create_parser()

    @staticmethod
    def _create_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="TopOne Proof of Reserves Verification Script", epilog="""Examples:
    python script.py <leaf_hash> <merkle_path>
    Full example with actual hashes:python script.py "7e8d8648656aeaa0c6" "36a99e593d250b741e1e4,25aa9b10a354010b" """,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('leaf_hash', help='Hash of your record in the MerkleTree ')
        parser.add_argument('merkle_path',
                            help='The hash path of your identifier in Merkle Tree with the format: "{hash1},{hash2}..."')

        return parser

    @staticmethod
    def verify_merkle_path2(leaf_hash: str, merkle_path: list) -> str:
        try:
            current_hash = binascii.unhexlify(leaf_hash)
            for i, path in enumerate(merkle_path):
                path_hash = path[1:]
                proof_bytes = binascii.unhexlify(path_hash)
                h = hashlib.sha256()
                if path[0] == "1":  # right leaf
                    h.update(current_hash)
                    h.update(proof_bytes)
                else:
                    h.update(proof_bytes)
                    h.update(current_hash)
                current_hash = h.digest()
                print(f"Level {i} hash: {current_hash.hex()}")
            return current_hash.hex()
        except binascii.Error as e:
            raise ValueError(f"Invalid hex format: {str(e)}")
        except Exception as e:
            raise ValueError(f"Verification failed: {str(e)}")


    @staticmethod
    def verify_merkle_path(leaf_hash: str, merkle_path: list[str]) -> str:
        """
        :param leaf_hash:  your hash_id
        :param merkle_path: merkle_path in your download file,formatted like: "{hash1},{hash2}..."'
        :return:  merkle root of the tree
        """
        try:
            current_hash = binascii.unhexlify(leaf_hash)
        except binascii.Error as e:
            raise ValueError(f"invalid leaf hash: {e}") from None
        for i, path in enumerate(merkle_path):
            path_hash = path[1:]
            try:
                proof_bytes = binascii.unhexlify(path_hash)
            except binascii.Error as e:
                raise ValueError(f"invalid merkle path {i}: {e}") from None
            h = hashlib.sha256()
            if path[0] ==0:
                h.update(current_hash)
                h.update(proof_bytes)
            else:
                h.update(proof_bytes)
                h.update(current_hash)
            current_hash = h.digest()

        return current_hash.hex()

    def run(self) -> None:
        args = self.parser.parse_args()
        try:
            merkle_path = list(args.merkle_path.split(","))
            root_hash = self.verify_merkle_path2(args.leaf_hash, merkle_path)
            print("targe root_hash:",root_hash)
        except Exception as e:
            print(f"verify_merkle_path failed:",e)


def main():
    verifier = MerkleVerification()
    verifier.run()


if __name__ == '__main__':
    main()
