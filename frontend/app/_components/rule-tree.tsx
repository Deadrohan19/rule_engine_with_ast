import React from 'react';
import { Tree, RawNodeDatum } from 'react-d3-tree';

interface ASTNode {
    type: string;
    op: string;
    attrType: string;
    left: ASTNode;
    right: ASTNode;
}

const textLayout = {
  vertical: {
    title: {
      textAnchor: 'start',
      x: 40,
    },
    attributes: {},
    attribute: {
      x: 40,
      dy: '1.2em',
    },
  },
  horizontal: {
    title: {
      textAnchor: 'start',
      y: 40,
    },
    attributes: {
      x: 0,
      y: 40,
    },
    attribute: {
      x: 0,
      dy: '1.2em',
    },
  },
};

const customNodeRenderer = ({ nodeDatum, orientation, toggleNode }: { nodeDatum: RawNodeDatum, orientation: 'vertical' | 'horizontal', toggleNode: () => void }) => {
  return (
    <>
      <circle r={20} onClick={toggleNode}></circle>
      <g className="rd3t-label">
        <text
          className="rd3t-label__title"
          {...textLayout[orientation].title}
        >
          {nodeDatum.name}
        </text>
        <text className="rd3t-label__attributes" {...textLayout[orientation].attributes}>
          {nodeDatum.attributes &&
            Object.entries(nodeDatum.attributes).map(([labelKey, labelValue], i) => (
              <tspan key={`${labelKey}-${i}`} {...textLayout[orientation].attribute}>
                {labelKey}: {labelValue}
              </tspan>
            ))}
        </text>
      </g>
    </>
  );
};



const transformToTree = (node: ASTNode): RawNodeDatum => {
    const treeNode = {
        name: node.type,
        attributes: node.attrType !== null ? {op: node.op, attrType: node.attrType } : {op: node.op},
    } as RawNodeDatum;

    if (node.type == 'comparision') {
        const left : RawNodeDatum = {
            name: node.left as unknown as string,
        }
        const right : RawNodeDatum = {
            name: node.right as unknown as string,
        }
        treeNode.children = [left, right];
        
        return treeNode;
    }

    treeNode.children = [transformToTree(node.left),transformToTree(node.right)]

    return treeNode;
};  

const RuleTree = ({ root } : { root: ASTNode}) => {
    const treeData = [transformToTree(root)];
    return (
        <Tree
            data={treeData}
            orientation="vertical"
            pathFunc="diagonal"
            renderCustomNodeElement={(props) => customNodeRenderer({ ...props, orientation: 'vertical' })}
            translate={{ x: 450, y: 100 }}  // Adjust initial position
        />
    );
};


export default RuleTree;
