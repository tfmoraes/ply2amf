import sys
import xml.etree.ElementTree as ET

import ply_reader


class AMFWriter:
    def __init__(self):
        self.meshes = []

    def add_mesh(self, mesh):
        self.meshes.append(mesh)

    def write(self, filename):
        root = ET.Element('amf')
        for mesh in self.meshes:
            self._add_object(root, mesh)
        with open(filename, 'w', encoding='utf8') as f:
            f.write(ET.tostring(root, encoding='utf8').decode('utf8'))

    def _add_object(self, parent, mesh):
        object_node = ET.SubElement(parent, 'object', id="1")
        self._add_mesh(object_node, mesh)

    def _add_mesh(self, parent, mesh):
        mesh_node = ET.SubElement(parent, 'mesh')
        self._add_vertices(mesh_node, mesh)
        self._add_volume(mesh_node, mesh)

    def _add_vertices(self, parent, mesh):
        vertices_node = ET.SubElement(parent, 'vertices')
        for vx, vy, vz in mesh.vertices:
            vertex_node = ET.SubElement(vertices_node, 'vertex')
            coordinates_node = ET.SubElement(vertex_node, 'coordinates')
            x_node = ET.SubElement(coordinates_node, 'x')
            x_node.text = str(vx)
            y_node = ET.SubElement(coordinates_node, 'y')
            y_node.text = str(vy)
            z_node = ET.SubElement(coordinates_node, 'z')
            z_node.text = str(vz)

    def _add_volume(self, parent, mesh):
        volume_node = ET.SubElement(parent, 'volume')
        for f0, f1, f2 in mesh.faces:
            triangle_node = ET.SubElement(volume_node, 'triangle')
            f0_node = ET.SubElement(triangle_node, 'v1')
            f0_node.text = str(f0)
            f1_node = ET.SubElement(triangle_node, 'v2')
            f1_node.text = str(f1)
            f2_node = ET.SubElement(triangle_node, 'v3')
            f2_node.text = str(f2)


def main():
    reader = ply_reader.PlyReader(sys.argv[1])
    reader.read()

    writer = AMFWriter()
    writer.add_mesh(reader)
    writer.write(sys.argv[2])


if __name__ == "__main__":
    main()
